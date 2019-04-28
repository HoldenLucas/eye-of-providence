import boto3
import json
import sys
import pprint
import decouple

class VideoDetect:
    jobId = ""
    rek = boto3.client("rekognition")
    queueUrl = "https://sqs.us-east-2.amazonaws.com/604089933659/JOB"
    roleArn = "arn:aws:iam::604089933659:role/Rekognition"
    topicArn = "arn:aws:sns:us-east-2:604089933659:AmazonRekognition-JOB"
    bucket = decouple.config("AWS_STORAGE_BUCKET_NAME")
    face_folder = "faces/"
    event_folder = "events/"
    collectionId = "guests"

    def makeCollection(self):
        self.rek.delete_collection(CollectionId=self.collectionId)
        return self.rek.create_collection(CollectionId=self.collectionId)

    # TODO: detect faces in image first to ensure just 1 face is present
    # TODO: check if face is already stored
    def indexFace(self, name: str):
        name = name.replace(" ", "_")
        return self.rek.index_faces(
            CollectionId=self.collectionId,
            Image={
                "S3Object": {"Bucket": self.bucket, "Name": self.face_folder + name}
            },
            ExternalImageId=name,
        )

    def deleteFace(self, id):
        return self.rek.delete_faces(CollectionId=self.collectionId, FaceIds=[str(id)])

    def listFaces(self):
        return self.rek.list_faces(CollectionId=self.collectionId)

    def main(self, event_date):

        jobFound = False
        sqs = boto3.client("sqs")

        response = self.rek.start_face_search(
            Video={
                "S3Object": {
                    "Bucket": self.bucket,
                    "Name": self.event_folder + event_date,
                }
            },
            CollectionId=self.collectionId,
            NotificationChannel={"RoleArn": self.roleArn, "SNSTopicArn": self.topicArn},
        )

        print("Start Job Id: " + response["JobId"])
        dotLine = 0
        while not jobFound:
            sqsResponse = sqs.receive_message(
                QueueUrl=self.queueUrl,
                MessageAttributeNames=["ALL"],
                MaxNumberOfMessages=10,
            )

            if sqsResponse:

                if "Messages" not in sqsResponse:
                    if dotLine < 20:
                        print(".", end="")
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    continue

                for message in sqsResponse["Messages"]:
                    notification = json.loads(message["Body"])
                    rekMessage = json.loads(notification["Message"])
                    print(rekMessage["JobId"])
                    print(rekMessage["Status"])
                    if str(rekMessage["JobId"]) == response["JobId"]:
                        print("Matching Job Found:" + rekMessage["JobId"])
                        jobFound = True

                        matches_stats = self.GetResultsFaceSearchCollection(rekMessage["JobId"])

                        sqs.delete_message(
                            QueueUrl=self.queueUrl,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                    else:
                        print(
                            "Job didn't match:"
                            + str(rekMessage["JobId"])
                            + " : "
                            + str(response["JobId"])
                        )
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(
                        QueueUrl=self.queueUrl, ReceiptHandle=message["ReceiptHandle"]
                    )

        print("done")
        return matches_stats

    def GetResultsFaceSearchCollection(self, jobId):
        maxResults = 10
        paginationToken = ""
        matches = set()
        total = set()

        finished = False

        while not finished:
            response = self.rek.get_face_search(
                JobId=jobId, MaxResults=maxResults, NextToken=paginationToken
            )

            for personMatch in response["Persons"]:

                total.add(personMatch["Person"]["Index"])

                print("Person Index: " + str(personMatch["Person"]["Index"]))
                print("Timestamp: " + str(personMatch["Timestamp"]))

                if "FaceMatches" in personMatch:
                    for faceMatch in personMatch["FaceMatches"]:

                        matches.add(faceMatch["Face"]["ExternalImageId"])

                        print("Face ID: " + faceMatch["Face"]["ExternalImageId"])
                        print("Similarity: " + str(faceMatch["Similarity"]))
                print()
            if "NextToken" in response:
                paginationToken = response["NextToken"]
            else:
                finished = True
            print()

        return (matches, len(total))


if __name__ == "__main__":
    analyzer = VideoDetect()
    pprint.pprint(analyzer.makeCollection())
    pprint.pprint(analyzer.listFaces()["Faces"])
#     analyzer.main()
