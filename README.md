# weixin_login
微信网页授权实现扫码登录
## 实现思路
1. 用户打开登录页, 客户端向服务端请求state值, 服务端生成随机字符串state, 并存入session和redis中, 然后将state返回给客户端
2. 将state值拼接到微信授权URL, 生成二维码, 显示在登录页
https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
3. 用户使用手机微信扫码, 确认授权登录, 跳转到步骤2中指定好的redirect_uri, 显示登录成功页面
4. redirect_uri对应的服务除了显示登录成功页面外, 还需要验证接受到的code，并在redis中保存对应state的验证信息
5. 登录页在显示二维码后会实时请求服务端, 确认redis中对应的state是否已被验证, 当确认验证后则登录成功, 之后就和微信网页授权的步骤一样了
