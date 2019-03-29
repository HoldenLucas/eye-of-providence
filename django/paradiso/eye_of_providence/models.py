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

    def get_absolute_url(self):
        return reverse("eye_of_providence:guest-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # =====
        analyzer = VideoDetect()
        analyzer.indexFace(str(self))
        pprint(analyzer.listFaces())

    def delete(self, *args, **kwargs):
        # analyzer = VideoDetect()
        # print("deleting guest")
        # pprint(analyzer.deleteFace(str(self)))
        # =====
        super().delete(*args, **kwargs)


def rename_event_video(instance, filename):
    return str(instance)


class Event(models.Model):
    date = models.DateTimeField()
    guests = models.ManyToManyField(Guest, blank=True)
    video = models.FileField(upload_to=rename_event_video, storage=EventStorage())

    def save(self, *args, **kwargs):
        print("Uploading video")
        super().save(*args, **kwargs)  # Call the "real" save() method.
        print("Done")
        # =====
        analyzer = VideoDetect()
        newstring = str(self).replace(" ", "_").replace(":", "")
        pprint(analyzer.main(newstring))

    def delete(self, *args, **kwargs):
        # analyzer = VideoDetect()
        # pprint(analyzer.delete_faces(CollectionId="guests", FaceIds=[str(self)]))
        # =====
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("eye_of_providence:event-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.date)
