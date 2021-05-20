from user.models import User



if __name__ == "__main__":
    a=User(
        userID="12345",
        Name="Zhang San",
        School="Physics",
        Group=1,
        password="12345",
        filename="ZhangSan File",
        Identity="Root"
        )

    a.save()