from enum import IntEnum


class CountryID(IntEnum):
    SELECT = -999999
    RUSSIA = 2


class SID(IntEnum):
    SELECT = -999999
    SAMARA = 1


class PID(IntEnum):
    SELECT = -999999
    # Cities
    ZHIGULEVSK = -485
    KINEL = -300
    NOVOKUIBYSHEVSK = -56
    OKTYABRSK = -451
    OTRADNIY = -328
    PROHVISTNEVO = -30
    SAMARA = -1
    SYZRAN = -224
    TOLYATTI = -232
    CHAPAEVSK = -242

    # Regions
    ALEKSEEVSKIY = 4
    BEZENCHUKSKIY = 5
    BOGATOVSKIY = 7
    BOLSHEGLUSHITSKIY = 1
    BORSKIY = 8
    VOLZHSKIY = 9
    ELHOVSKIY = 10
    ISAKLINSKIY = 12
    KINELSKIY = 14
    KINEL_CHERKASSKIY = 58
    KLYAVLINSKIY = 15
    KOSHKINSKIY = 16
    KRASNOARMEISKIY = 2
    KRASNOYARSKIY = 17
    NEFTEGORSKIY = 18
    PESTRAVSKIY = 19
    POHVISTNEVSKIY = 20
    PRIVOLZHSKIY = 3
    SERGIEVSKIY = 21
    STAVROPOLSKIY = 22
    SYZRANSKIY = 23
    HVOROSTYANSKIY = 24
    CHELNO_VERSHINSKIY = 25
    SHENTALINSKIY = 26
    SHIGONSKIY = 27


class CityNumber(IntEnum):
    SELECT = -999999
    SAMARA = 1


class StudyFormatType(IntEnum):
    SELECT = -999999
    PRESCHOOL = 1
    COMMON = 2
    ADDITIONAL = 3


class SchoolID(IntEnum):
    """Check at https://github.com/VityaSchel/asurso/blob/master/LOGINIDS.md#scid-id-образовательной-организации"""

    SELECT = -999999
    pass
