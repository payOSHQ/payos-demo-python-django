import hashlib
import hmac

from typing import Union
from collections import OrderedDict

def convertObjToQueryStr(obj: dict) -> str:
    """
    Chuyển đổi đối tượng JSON thành chuỗi truy vấn URL.
    """
    query_string = []

    for key, value in obj.items():
        value_as_string = str(value) if isinstance(value, (str, int, float, bool)) else value
        query_string.append(f"{key}={value_as_string}")

    return "&".join(query_string)

def sortObjDataByKey(obj: Union[dict, list]) -> Union[dict, list]:
    """
    Sắp xếp đối tượng JSON theo khóa.
    """
    if isinstance(obj, dict):
        ordered_object = dict(sorted(obj.items()))
        return ordered_object
    elif isinstance(obj, list):
        # Nếu là danh sách, sắp xếp từng đối tượng trong danh sách
        return [convertObjToQueryStr(item) for item in obj]
    else:
        return obj

def createSignatureFromObj(data, key):
    """
    Tạo chữ ký từ đối tượng JSON.
    """
    sorted_data_by_key = sortObjDataByKey(data)
    data_query_str = convertObjToQueryStr(sorted_data_by_key)

    # Sử dụng hashlib.sha256 thay thế cho crypto.createHmac
    data_to_signature =  hmac.new(key.encode("utf-8"), msg=data_query_str.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()

    return data_to_signature

def createSignatureOfPaymentRequest(data, key):
    """
    Tạo chữ ký của yêu cầu thanh toán.
    """
    amount = data["amount"]
    cancel_url = data["cancelUrl"]
    description = data["description"]
    order_code = data["orderCode"]
    return_url = data["returnUrl"]

    data_str = f"amount={amount}&cancelUrl={cancel_url}&description={description}&orderCode={order_code}&returnUrl={return_url}"
    data_to_signature =  hmac.new(key.encode("utf-8"), msg=data_str.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    return data_to_signature