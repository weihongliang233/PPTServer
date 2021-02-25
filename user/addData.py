
from . import models



if __name__ == "__main__":
    a=models.User(
        userID="320180934321",
        Name="Zhang San",
        School="Physics",
        Group=1,
        password="320180934321",
        filename="ZhangSan File",
        Identity="Student"
        )

    a.save()

    a=models.User(
        userID="320180934562",
        Name="Li si",
        School="Bio",
        Group=2,
        password="3201809343562",
        filename="LiSi File",
        Identity="Teacher"
        )

    a.save()