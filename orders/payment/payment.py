# from __future__ import annotations
import base64
import datetime
import json

import requests
from requests.auth import HTTPBasicAuth

from .account_type import AccountType


class MpesaClient:
    """
    visit https://developer.safaricom.co.ke/Documentation for more
    :param BusinessShortCode(shot code): This is organizations shortcode (Paybill or
        Buygoods - A 5 to 7 digit account number) used to identify an
        organization and receive the transaction.
        Shortcode (5 to 7 digits) e.g. 654321
    :attr Timestamp ->This is the Timestamp of the transaction,
        normally in the format of YEAR+MONTH+DATE+HOUR+MINUTE+SECOND (YYYYMMDDHHMMSS)
        Each part should be atleast two digits apart from the year which takes four digits.
    :attr TransactionType -> This is the transaction type that is used to identify the
        transaction when sending the request to M-Pesa. The transaction type for M-Pesa
        Express is "CustomerPayBillOnline"
        CustomerPayBillOnline for paybill and CustomerBuyGoodsOnline for till/nuy goods
    :attr PartyA -> The phone number sending money. The parameter expected is a Valid Safaricom
        Mobile Number that is M-Pesa registered in the format 2547XXXXXXXX
        MSISDN (12 digits Mobile Number) e.g. 2547XXXXXXXX
    :attr PartyB -> The organization receiving the funds. The parameter expected is
        a 5 to 7 digit as defined on the Shortcode description above. This can be the
         same as BusinessShortCode value above.
    :attr CallBackURL -> A CallBack URL is a valid secure URL that is used to receive
        notifications from M-Pesa API. It is the endpoint to which the results will
        be sent by M-Pesa API.
        NB:TT MUST BE SECURE(HTTPS)
    :attr AccountReference -> Account Reference: This is an Alpha-Numeric parameter that is
        defined by your system as an Identifier of the transaction for CustomerPayBillOnline
        transaction type. Along with the business name, this value is also displayed to the
        customer in the STK Pin Prompt message. Maximum of 12 characters.
    :attr TransactionDesc -> This is any additional information/comment that can be sent
        along with the request from your system. Maximum of 13 Characters.
    :attr phone_number -> The Mobile Number to receive the STK Pin Prompt.
        This number can be the same as PartyA value above.
        Must follow format 2547XXXXXXXX
    :attr amount -> This is the Amount transacted normally
        a numeric value. Money that customer pays to the Shortcode.
        NB: Only whole numbers are supported.
    """

    class Builder:
        def __init__(self):
            self._auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
            self._consumer_key = None
            self._consumer_secret = None
            self._account_type = AccountType.TILL
            self._query_params = {"grant_type": "client_credentials"}
            # self._phone_number = None
            # self._amount = decimal.Decimal(0.0)
            self._call_back_url = ""
            self._short_code = None
            self._description = ""
            self._business_name = None
            self._pass_key = None
            self._stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        def add_stk_push_url(self, url: str) -> "Builder":
            """
            Url for processing stk push.Its optional,
            the default is set to: https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
            """
            self._stk_push_url = url
            return self

        def add_business_name(self, name: str) -> "Builder":
            """
            Account Reference or business name: This is an Alpha-Numeric parameter that is
            defined by your system as an Identifier of the transaction for CustomerPayBillOnline
            transaction type. Along with the business name, this value is also displayed to the
            customer in the STK Pin Prompt message. Maximum of 12 characters.
            """
            if len(name) > 12:
                # TODO THROW AN ILLEGAL ARGUMENT EXCEPTION
                pass
                # raise
            self._business_name = name
            return self

        def add_business_short_code(self, short_code: int) -> "Builder":
            """
            BusinessShortCode(shot code): This is organizations shortcode (Paybill or
            Buygoods - A 5 to 7 digit account number) used to identify an
            organization and receive the transaction.
            Shortcode (5 to 7 digits) e.g. 654321
            """
            self._short_code = short_code
            return self

        def add_call_back_url(self, call_back_url: str) -> "Builder":
            self._call_back_url = call_back_url
            return self

        def add_description(self, description: str) -> "Builder":
            """
            This is any additional information/comment that can be sent
            along with the request from your system. Maximum of 13 Characters.
            Alpha-Numeric
            """
            self._description = description
            return self

        # def add_phone_number(self, phone: int) -> "Builder":
        #     self._phone_number = phone
        #     return self

        # def add_amount(self, amount: decimal.Decimal) -> "Builder":
        #     self._amount = amount
        #     return self

        def add_query_param(self, query_param: dict) -> "Builder":
            """
            client_credentials is the most important query parameter,as the name suggests
            its responsible for querying the access token, the default is set to
            {"grant_type": "client_credentials"}
            if grant type param is wrong, you receive a :
            Invalid grant type passed error from server with response code 400.008.02
            """
            self._query_params.update(query_param)
            return self

        def add_auth_url(self, url: str) -> 'Builder':
            """
            Url for authentication and obtaining access token to be used in other api
            Optional, the default is set to: "https://sandbox.safaricom.co.ke/oauth/v1/generate"
            """
            self._auth_url = url
            return self

        def add_credentials(self, consumer_key: str, consumer_secret: str, pass_key: str) -> 'Builder':
            self._consumer_key = consumer_key
            self._consumer_secret = consumer_secret
            self._pass_key = pass_key
            return self

        def set_account_type(self, account_type: AccountType) -> "Builder":
            """
            Default is till
            """
            self._account_type = account_type
            return self

        def build(self) -> "MpesaClient":
            # TODO ADD VALIDATION MECHANISM B4 BUILD
            return MpesaClient(
                auth_url=self._auth_url,
                consumer_key=self._consumer_key,
                consumer_secrete=self._consumer_secret,
                account_type=self._account_type,
                query_params=self._query_params,
                # phone_number=self._phone_number,
                # amount=self._amount,
                call_back_url=self._call_back_url,
                description=self._description,
                short_code=self._short_code,
                business_name=self._business_name,
                pass_key=self._pass_key,
                stk_push_url=self._stk_push_url
            )

    def __init__(
            self,
            auth_url: str,
            consumer_key: str,
            consumer_secrete: str,
            account_type: AccountType,
            query_params: dict,
            # phone_number: int,
            # amount: decimal.Decimal,
            call_back_url: str,
            description: str,
            short_code: int,
            business_name: str,
            pass_key: str,
            stk_push_url: str
    ):
        self._stk_push_url = stk_push_url
        self._pass_key = pass_key
        self._short_code = short_code
        self._auth_url = auth_url
        self._call_back_url = call_back_url
        self._description = description
        self._business_name = business_name
        # self._amount = amount
        # self._phone_number = phone_number
        self._querystring = query_params
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secrete
        self._account_type = account_type
        self._basic_auth = self._get_basic_auth()
        self._payload = ""
        self._time_format_string = "%Y%m%d%H%M%S"

    def _get_access_token(self) -> str:
        """
        Access token to access other APIs
        Retrieved by first performing basic authentication with customer key and secrete
        This token prevents the client from authenticating each time a request is made
        The token leaves only for an hour (3599 seconds)
        sample response:
        {
            "access_token": "k3q5A05OjOggFcpFkLxtqGF41bfq",
            "expires_in": "3599"
        }
        """
        response = requests.request(
            "GET",
            url=self._auth_url,
            data=self._payload,
            # headers=headers,
            auth=self._basic_auth,
            params=self._querystring
        )
        return json.loads(response.text)["access_token"]

    def _get_bearer_auth(self):
        """
        Given the access token for use by other apis within one hour after which it expires
        """
        return {"Authorization": f"Bearer {self._get_access_token()}"}

    def _get_basic_auth(self) -> HTTPBasicAuth:
        """
        forms a Basic Authorization header using consumer key and consumer
        secret obtained from safari developer site after creating a sandbox app
        If either the key or secret is wrong, you will receive:
        Invalid Authentication passed with response code 400.008.01

        The request's HTTPBasicAuth creates a basic auth header for you
        syntax for auth header: 'Authorization': <type> <token>
        Where : type could be Bearer, Basic, Hashed,e.t.c ie its like the key and specifies authentication type
            : token is the value , used for authentication

        For Basic auth the value takes "username:password" i.e consumer_key:consumer_secrete which is then
        encoded to base64 to lool like:
            'Authorization': 'Basic mkjJDKFVndggc'

        Bellow class works similar to this sample code similar to:
        Note working though
        You must not first encode to ascii, you could encode directly
        cred_ascii_encoded = f"{self._consumer_key}: {self._consumer_secret}".encode('ascii')
        cred_b64_encoded = base64.b64encode(cred_ascii_encoded)
        header = {
            'Authorization': f'Basic {cred_b64_encoded.decode("utf-8")}'
        }

        """
        return HTTPBasicAuth(self._consumer_key, self._consumer_secret)

    def _get_password(self):
        """
        This is the password used for encrypting the request sent: A
        base64 encoded string. (The base64 string is a combination of Shortcode+Passkey+Timestamp)
        base64.encode(Shortcode+Passkey+Timestamp)
        """
        time_stamp = datetime.datetime.now().strftime(self._time_format_string)
        # First encode to ascii to prevent unicode errors
        data_to_encode = str(self._short_code) + self._pass_key + time_stamp
        encoded_password = base64.b64encode(data_to_encode.encode('ascii'))
        return encoded_password

    def _get_payload(self, phone: int, amount: int) -> dict:
        """
            Packages all the information about a transaction into a dictionary

        """
        return {
            "BusinessShortCode": self._short_code,
            "Password": self._get_password(),
            "Timestamp": datetime.datetime.now().strftime(self._time_format_string),
            "TransactionType": self._get_transaction_type(),
            "Amount": amount,
            "PartyA": phone,
            "PartyB": self._short_code,
            "PhoneNumber": phone,
            "CallBackURL": self._call_back_url,
            "AccountReference": self._business_name,
            "TransactionDesc": self._description
        }

    def _get_transaction_type(self):
        """
        CustomerPayBillOnline for paybill
         CustomerBuyGoodsOnline for till/nuy goods
        """
        return "CustomerBuyGoodsOnline" if self._account_type == AccountType.TILL else "CustomerPayBillOnline"

    def trigger_stk_push(self, amount: int, phone_number: int):
        """
        :param phone_number -> The Mobile Number to receive the STK Pin Prompt.
            This number can be the same as PartyA value above.
            Must follow format 2547XXXXXXXX
        :param amount -> This is the Amount transacted normally
            a numeric value. Money that customer pays to the Shortcode.
        NB: Only whole numbers are supported.

        Response:
        :resp MerchantRequestID -> This is a global unique Identifier for any submitted payment request.
            String e.g 16813-1590513-1
        :resp CheckoutRequestID -> This is a global unique identifier of the processed checkout
            transaction request.String e.g ws_CO_DMZ_12321_23423476
        :resp ResponseDescription -> Response description is an acknowledgment message from the API
            that gives the status of the request submission usually maps to a specific ResponseCode
            value. It can be a Success submission message or an error description.String e.g
            The service request has failed, The service request has been accepted successfully,
             Invalid Access Token
        :resp ResponseCode -> This is a Numeric status code that indicates the status of the
            transaction submission. 0 means successful submission and any other code means an error occurred.
            Numeric	or 404.001.03
        :resp CustomerMessage -> This is a message that your system can display to the Customer as an
            acknowledgement of the payment request submission.String E.g: Success. Request accepted for processing.

        sample response: {
            "MerchantRequestID": "25353-1377561-4",
            "CheckoutRequestID": "ws_CO_26032018185226297",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing"
        }

        :error requestId ->This is a unique requestID for the payment request
            String	e.g 16813-15-1
        :error errorCode -> This is a predefined code that indicates the reason for
            request failure. This are defined in the Response Error Details below.
            The error codes maps to specific error message as illustrated in the Response
            Error Details below.	String e.g	404.001.04
        :error errorMessage ->This is a short descriptive message of the failure reason.
            String e.g Invalid Access Token

        """
        header = {'Content-Type': 'application/json'}
        header.update(self._get_bearer_auth())
        response = requests.request(
            method="POST",
            url=self._stk_push_url,
            data=self._get_payload(
                phone=phone_number,
                amount=amount
            ),
            headers=header
        )
        return json.loads(response.text)

    def __doc__(self):
        """
        For more visit:
        This is the results that is received once the payment has been processed successfully by M-PESA.
        This result is received by the Merchant (Partner) on their callback URL from the request body.

                {
           "Body": {
              "stkCallback": {
                 "MerchantRequestID": "29115-34620561-1",
                 "CheckoutRequestID": "ws_CO_191220191020363925",
                 "ResultCode": 0,
                 "ResultDesc": "The service request is processed successfully.",
                 "CallbackMetadata": {
                    "Item": [{
                       "Name": "Amount",
                       "Value": 1.00
                    },
                    {
                       "Name": "MpesaReceiptNumber",
                       "Value": "NLJ7RT61SV"
                    },
                    {
                       "Name": "TransactionDate",
                       "Value": 20191219102115
                    },
                    {
                       "Name": "PhoneNumber",
                       "Value": 254708374149
                    }]
                 }
              }
           }
        }

        Description:
        :Body: his is the root key for the entire Callback message.type JSON Object e.g{"Body":{ }}
        stkCallback: This is the first child of the Body.type JSON Object
        :MerchantRequestID: This is a global unique Identifier for any submitted payment request.
        This is the same value returned in the acknowledgement message of the initial request.type String
        e.g 29115-34620561-1
        :CheckoutRequestID:This is a global unique identifier of the processed checkout transaction request.
         This is the same value returned in the acknowledgement message of the initial request.
        type String e.g ws_CO_191220191020363925
        :ResultCode: This is a numeric status code that indicates the status of the transaction processing.
        0 means successful processing and any other code means an error occurred or the transaction failed.
        type Numeric e.g 0, 1032
        :ResultDesc: Result description is a message from the API that gives the status of the request
        processing, usually maps to a specific ResultCode value. It can be a Success processing message
        or an error description message.type String E.g: 0: The service request is processed successfully.
        1032: Request cancelled by user
        :CallbackMetadata: This is the JSON object that holds more details for the transaction.
        It is only returned for Successful transaction. type JSON Object
        :Item: This is a JSON Array, within the CallbackMetadata, that holds additional transaction
        details in JSON objects. Since this array is returned under the CallbackMetadata, it is only
        returned for Successful transaction. type JSON Array
        :Amount: This is the Amount that was transacted.type Decimal e.g 10500.5
        :MpesaReceiptNumber: This is the unique M-PESA transaction ID for the payment request.
        Same value is sent to customer over SMS upon successful processing.type String LHG31AA5TX
        :Balance: This is the Balance of the account for the shortcode used as partyB type Decimal
        e.g 32009.9
        :TransactionDate: This is a timestamp that represents the date and time that the transaction
        completed in the formart YYYYMMDDHHmmss type TimeStamp e.g 20170827163400
        :PhoneNumber: This is the number of the customer who made the payment.type PhoneNumber e.g 0722000000

        Whenever you receive an error in your callback url, the unsuccessful transaction will
        have a body results as below and the details of the error will be captured under the
        Items ResultCode and ResultDesc; Click here to see the list of possible Lipa na M-PESA
        online errors

        {
           "Body": {
              "stkCallback": {
                 "MerchantRequestID": "29115-34620561-1",
                 "CheckoutRequestID": "ws_CO_191220191020363925",
                 "ResultCode": 1032,
                 "ResultDesc": "Request cancelled by user."
              }
           }
        }
        """
