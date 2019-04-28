from django.db import models
from pprint import pprint
from paradiso.storage_backends import FaceStorage, EventStorage
from django.urls import reverse, reverse_lazy
from rekognition import VideoDetect

def rename_guest_photo(instance, filename):
    return str(instance)

class Guest(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    photo = models.ImageField(upload_to=rename_guest_photo, storage=FaceStorage())
    external_id = models.CharField(max_length=100, null=True)

    # def get_absolute_url(self):
    #     return reverse("eye_of_providence:guest-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        analyzer = VideoDetect()
        analyzer.indexFace(str(self))
        face_list = analyzer.listFaces()["Faces"]
        # if there is no external id, get it
        if self.external_id == None:
            for face in face_list:
                if face['ExternalImageId'] == self.name:
                    self.external_id = face["FaceId"]
                    break
            self.save()

    def delete(self, *args, **kwargs):
        analyzer = VideoDetect()
        analyzer.deleteFace(self.external_id)

        super().delete(*args, **kwargs)


def rename_event_video(instance, filename):
    return str(instance)

class Event(models.Model):
    name = models.CharField(max_length=30)
    known_guests = models.ManyToManyField(Guest, blank=True)
    potential_faces = models.IntegerField(blank=True, null=True)

    video = models.FileField(upload_to=rename_event_video, storage=EventStorage())

    def analyse(self):
        analyzer = VideoDetect()
        matches = analyzer.main(str(self))

        self.potential_faces = matches[1]

        for guest_name in matches[0]:
            guest = Guest.objects.get(name=guest_name)
            self.known_guests.add(guest)

        self.save()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     super().delete(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("eye_of_providence:event-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)
