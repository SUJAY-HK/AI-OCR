from django.db import models
from django.contrib.auth.models import User
import random

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class Book(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_books")
    collaborators = models.ManyToManyField(User, related_name="collaborating_books")
    created_at = models.DateTimeField(auto_now_add=True)

class UserColor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default=random_color)

    class Meta:
        unique_together = ("book", "user")

class Sketch(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sketches")
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="sketches/", blank=True, null=True)
    strokes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for OCR and audio
    ocr_explanation = models.TextField(blank=True, null=True)  # Store the explanation text
    audio_summary = models.FileField(upload_to="audio_summaries/", blank=True, null=True)  # Store audio file
    audio_generated_at = models.DateTimeField(blank=True, null=True)  # Track when audio was generated
    
    def __str__(self):
        return f"{self.name} - {self.book.name}"