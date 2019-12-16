from django.test import TestCase

# Create your tests here.

#
# AlipayClient alipayClient = new DefaultAlipayClient("https://openapi.alipaydev.com/gateway.do", APP_ID, APP_PRIVATE_KEY, "json", CHARSET, ALIPAY_PUBLIC_KEY, "RSA2");
# AlipayTradePrecreateRequest request = new AlipayTradePrecreateRequest();
# AlipayTradePrecreateModel model = new AlipayTradePrecreateModel();
# request.setBizModel(model);
# model.setOutTradeNo(System.currentTimeMills());
# model.setTotalAmount("88.88");
# model.setSubject("Iphone6 16G");
# AlipayTradePrecreateResponse response = alipayClient.execute(request);
# System.out.print(response.getBody());
# System.out.print(response.getQrCode());
from alipay.aop.api import AlipayClientConfig

a = AlipayClientConfig()