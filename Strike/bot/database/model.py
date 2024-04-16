from peewee import Model, CharField, BigIntegerField, SqliteDatabase, TextField, DateTimeField, AutoField

db = SqliteDatabase('my_database.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

    def to_dict(self):
        return self.__data__


class table1(BaseModel):
    user_id = TextField()
    id_key = AutoField()
    actType = CharField()
    objNum = CharField()
    start_date = TextField()
    start_time = TextField()
    end_time = TextField()
    period_time = CharField()
    guestName = TextField()
    guestNumber = TextField()
    guestinfo = TextField()
    guestSkidka = CharField()
    pay = TextField()
    createTime = TextField()
    editTime = DateTimeField(null=True)

class tableCoach(BaseModel):
    id_key = TextField()
    user_id = TextField()
    nameCoach = TextField()
    dateTraining = TextField()
    timeTraining = TextField()
    endtimeTraining = TextField()
    period_time = TextField()
    objNum = CharField()
    coachConfirm = TextField()
    guestName = TextField()
    guestNumber = TextField()
    source = CharField(default="брони")

class schedule_coach(BaseModel):
    id_key = AutoField()
    objNum = TextField()
    coachName = TextField()
    dateTraining = TextField()
    timeTraining = TextField()
    endtimeTraining = TextField()
    period_time = TextField()
    nameUser = TextField()
    numberUser = TextField()
    source = CharField(default="расписание")

class Regular_customer(BaseModel):
    id_key = AutoField()
    userName = TextField()
    userNumber = TextField()


class Coach_list(BaseModel):
    actType = TextField()
    user_id = TextField()
    nameCoach = TextField()
    numberCoach = TextField()


def create_tables():
    db.create_tables([table1])
    db.create_tables([tableCoach])
    db.create_tables([schedule_coach])
    db.create_tables([Regular_customer])
    db.create_tables([Coach_list])


create_tables()

