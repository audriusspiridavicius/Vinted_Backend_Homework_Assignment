import pytest
from delivery_rule import BasicDeliveryRule
from enums import DeliveryProviderEnum, PackageSizeEnum


LP_S = 1.5
LP_M = 4.9
LP_L = 6.9

MR_S = 2
MR_M = 3
MR_L = 4


@pytest.fixture
def delivery_rules():
    
    
    
    return [
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.S, LP_S),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.M, LP_M),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.L, LP_L),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.S, MR_S),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.M, MR_M),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.L, MR_L),
    ]