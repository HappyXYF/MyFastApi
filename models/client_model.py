
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Client(BaseModel):
    ClientID: Optional[int] = None
    ClientCode: Optional[str] = None
    ClientName: str
    ClientShortName: Optional[str] = None
    ClientDoubleIdentity: Optional[bool] = None
    ClientShortCode: Optional[str] = None
    ClientLevel: Optional[int] = None
    ClientProperty: Optional[int] = None
    ClientLinkman: Optional[str] = None
    ClientTel: Optional[str] = None
    ClientFax: Optional[str] = None
    ClientAddress: Optional[str] = None
    ClientPostcode: Optional[str] = None
    ClientWebsite: Optional[str] = None
    ClientDescription: Optional[str] = None
    ClientMob: Optional[str] = None
    ClientLinkmanPosition: Optional[str] = None
    ClientStatus: Optional[int] = None
    ClientBank: Optional[str] = None
    ClientBankaccount: Optional[str] = None
    ClientTaxno: Optional[str] = None
    ClientCredit: Optional[float] = None
    ClientIsExpressCorp: Optional[bool] = None
    ClientLegalPerson: Optional[str] = None
    OwnerID: Optional[int] = None
    ClientCategory: Optional[int] = None
    ClientOrgID: Optional[int] = None
    ClientProvinceID: Optional[int] = None
    ClientCityID: Optional[int] = None
    ClientAreaID: Optional[int] = None
    ClientMarketPlaceID: Optional[int] = None
    ClientCategoryID: Optional[int] = None
    ClientBusinessScope: Optional[str] = None
    ClientSetMthod: Optional[int] = None
    ClientPayWay: Optional[int] = None
    ClientSalesDiscount: Optional[float] = None
    ClientClass: Optional[int] = None
    ClientCompanyName: Optional[str] = None
    ClientBirthday: Optional[datetime] = None

    class Config:
        from_attributes = True
