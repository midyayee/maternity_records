#!/usr/bin/env python
import enum
from typing import Optional
from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from models import Base, BaseModel

class Choices(enum.Enum):
    YES = 'yes'
    NO = 'no'
    NA= 'na'
    UNKNOWN = 'unknown'

class GenderIdentity(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    NON_BINARY = 'non_binary'


class Clients(Base, BaseModel):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_num:Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]] = mapped_column(String(255))
    family_name: Mapped[str] = mapped_column(String(255))
    date_of_birth: Mapped[str] = mapped_column(DateTime)
    street_address: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    emergency_contact_name: Mapped[str] = mapped_column(String(255))
    emergency_contact_phone: Mapped[str] = mapped_column(String(255))
    emergency_contact_relation: Mapped[str] = mapped_column(String(255))
    emergency_contact_address: Mapped[str] = mapped_column(String(255))

class ClientReg(Base, BaseModel):
    __tablename__ = 'registration_info'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_num:Mapped[str] = mapped_column(ForeignKey('clients.patient_num'))
    gender_identity: Mapped[GenderIdentity]
    sexual_orientation: Mapped[str] = mapped_column(String(255))
    ethinicity: Mapped[str] = mapped_column(String(255))
    preferred_language: Mapped[str] = mapped_column(String(255))
    gp_name: Mapped[str] = mapped_column(String(255))
    gp_phone: Mapped[str] = mapped_column(String(255))
    gp_address: Mapped[str] = mapped_column(String(255))
    gp_email: Mapped[str] = mapped_column(String(255))
    long_term_conditions: Mapped[str] = mapped_column(String(255))
    medications: Mapped[str] = mapped_column(String(255))
    allergies: Mapped[str] = mapped_column(String(255))
    heart_conditions: Mapped[Choices]
    diabetes: Mapped[Choices]
    high_blood_pressure: Mapped[Choices]
    epilepsy: Mapped[Choices]
    asthma: Mapped[Choices]
    stomach_bowel_conditions: Mapped[Choices]
    cancer: Mapped[Choices]
    mental_health_conditions: Mapped[Choices]
    substance_abuse: Mapped[Choices]
    other_conditions: Mapped[str] = mapped_column(String(255))
    alcoholism: Mapped[Choices]
    smoking: Mapped[Choices]
    family_history: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())




