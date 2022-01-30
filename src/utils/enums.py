import enum


class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class BloodGroupEnum(str, enum.Enum):
    ap = "A+"
    an = "A-"
    bp = "B+"
    bn = "B-"
    op = "O+"
    on = "O-"
    abp = "AB+"
    abn = "AB-"
