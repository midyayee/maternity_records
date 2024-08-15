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

class Urea(enum.Enum):
    zero = 0
    one_plus = '1+'
    two_plus= '2+'
    four_plus = '4+'
    no_test = 'no_test'


class Culture(enum.Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    PENDING = 'PENDING'

class PregnancyReg(Base, BaseModel):
    __tablename__ = 'preg_reg'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_num:Mapped[str] = mapped_column(ForeignKey('clients.patient_num'))
    pregnancy_num: Mapped[str] = mapped_column(String(255), unique=True)
    date_of_lmp: Mapped[str] = mapped_column(DateTime)
    edd: Mapped[str] = mapped_column(DateTime)
    weight: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    type_of_last_delivery: Mapped[Optional[str]] = mapped_column(String(255))
    outcome_of_last_delivery: Mapped[Optional[str]] = mapped_column(String(255))
    expected_delivery_facility: Mapped[str] = mapped_column(String(255))
    expected_delivery_facility_address: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())



class PregRiskAssessment(Base, BaseModel):
    __tablename__ = 'preg_risk'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    smokes_more_than_10_cigarettes_per_day: Mapped[Choices]
    less_than_2_years_since_last_pregnancy: Mapped[Choices]
    offered_hiv_counselling: Mapped[Choices]
    substance_abuse: Mapped[Choices]
    adolescent: Mapped[Choices]
    inadequate_nutrition: Mapped[Choices]
    domestic_violence: Mapped[Choices]
    mental_health_conditions: Mapped[Choices]
    inadequate_finances: Mapped[Choices]
    inadequate_housing: Mapped[Choices]
    inadequate_social_support: Mapped[Choices]
    less_than_high_school_education: Mapped[Choices]
    significant_learning_disability: Mapped[Choices]
    abnormal_pap_smear: Mapped[Choices]
    anemia: Mapped[Choices]
    bmi_over_30: Mapped[Choices]
    gestational_diabetes: Mapped[Choices]
    history_of_cervical_uterine_infections: Mapped[Choices]
    history_of_infant_with_neurolgical_defects: Mapped[Choices]
    history_of_infertility: Mapped[Choices]
    inadequate_prenatal_care: Mapped[Choices]
    incompetent_cervix: Mapped[Choices]
    IUGR: Mapped[Choices]
    multiple_gestation: Mapped[Choices]
    two_or_more_spontaneous_abortions: Mapped[Choices]
    rh_sensitization: Mapped[Choices]
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())


class PregFollowUp(Base, BaseModel):
    __tablename__ = 'preg_followup'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    date_of_visit: Mapped[str] = mapped_column(DateTime, default=func.now())
    gestational_age:Mapped[str] = mapped_column(String(255))
    weight: Mapped[int] = mapped_column(Integer)
    bp: Mapped[str] = mapped_column(String(255))
    fundal_height: Mapped[int] = mapped_column(Integer)
    fetal_heart_rate: Mapped[int] = mapped_column(Integer)
    proteinuria: Mapped[Urea]
    urine_culture: Mapped[Culture]
    iron: Mapped[Choices]
    folate: Mapped[Choices]
    calcium: Mapped[Choices]
    multivitamins: Mapped[Choices]
    other_symptoms: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())


class PregLabor(Base, BaseModel):
    __tablename__ = 'preg_labor'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    date_of_admission: Mapped[str] = mapped_column(DateTime, default=func.now())
    admission_time : Mapped[str] = mapped_column(String(30))
    time_active_labor_started: Mapped[str] = mapped_column(String(30))
    time_membranes_ruptured: Mapped[str] = mapped_column(String(30))
    time_second_stage_started: Mapped[str] = mapped_column(String(30))
    time_of_delivery: Mapped[str] = mapped_column(String(30))
    oxytocin_time_given: Mapped[str] = mapped_column(String(30))
    placenta_complete: Mapped[Choices]
    live_birth: Mapped[Choices]
    still_birth: Mapped[Choices]
    neonatal_death: Mapped[Choices]
    maternal_death: Mapped[Choices]
    resuscitation: Mapped[Choices]
    maternal_transfusion: Mapped[Choices]
    birth_weight: Mapped[int] = mapped_column(Integer)
    apgar1: Mapped[int] = mapped_column(Integer)
    apgar5: Mapped[int] = mapped_column(Integer)
    mode_of_delivery: Mapped[str] = mapped_column(String(255))
    gestational_age: Mapped[str] = mapped_column(String(255))
    more_than_one_baby: Mapped[Choices]
    fetal_lie: Mapped[str] = mapped_column(String(255))
    fetal_presenation: Mapped[str] = mapped_column(String(255))
    blood_pressure : Mapped[str] = mapped_column(String(255))
    temperature: Mapped[int] = mapped_column(Integer)
    pulse: Mapped[int] = mapped_column(Integer)
    problem: Mapped[str] = mapped_column(String(255))
    action_taken: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())

class PregPartograph(Base, BaseModel):
    __tablename__ = 'preg_partograph'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    hours_since_ruputured_membrance: Mapped[int] = mapped_column(Integer)
    rapid_assessment: Mapped[str] = mapped_column(String(255))
    vaginal_bleeding: Mapped[Choices]
    amniotic_fluid: Mapped[Choices]
    fetal_heart_rate: Mapped[str] = mapped_column(String(255))
    contractions_in_10_minutes: Mapped[str] = mapped_column(String(255))
    urine_voided: Mapped[Choices]
    pulse: Mapped[int] = mapped_column(Integer)
    blood_pressure: Mapped[str] = mapped_column(String(255))
    cervical_dilation: Mapped[str] = mapped_column(String(255))
    time_of_placental_delivery: Mapped[str] = mapped_column(String(255))
    oxytocin_time_given: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())


class PregPostPartum(Base, BaseModel):
    __tablename__ = 'preg_postpartum'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    date_of_visit: Mapped[str] = mapped_column(DateTime, default=func.now())
    weight: Mapped[int] = mapped_column(Integer)
    bp: Mapped[str] = mapped_column(String(255))
    nutrition: Mapped[str] = mapped_column(String(255))
    family_planning: Mapped[str] = mapped_column(String(255))
    breastfeeding: Mapped[Choices]
    danger_signs: Mapped[Choices]
    ART: Mapped[Choices]
    BCG: Mapped[Choices]
    OPV: Mapped[Choices]

class Death(Base, BaseModel):
    __tablename__ = 'preg_death'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_num:Mapped[str] = mapped_column(ForeignKey('preg_reg.pregnancy_num'))
    date_of_death: Mapped[str] = mapped_column(DateTime, default=func.now())
    time_of_death: Mapped[str] = mapped_column(String(30))
    primary_cause_of_death: Mapped[str] = mapped_column(String(255))
    secondary_cause_of_death: Mapped[str] = mapped_column(String(255))
    other_contributing_factors: Mapped[str] = mapped_column(String(255))
    birth_weight_if_infant_death: Mapped[int] = mapped_column(Integer)
    gestational_age: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[str] = mapped_column(DateTime, default=func.now())