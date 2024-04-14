from enum import Enum


class StatusCustomer(Enum):
    exist = 1
    not_exist = 2
    error = 3
    not_full_profile = 4
