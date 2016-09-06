# Flask blog
v1.0
Flask搭建的博客，演示地址：http://www.kurting.cn

部署于SAE

## 说明
1. config.yaml、index.wsgi  文件为sae部署所需文件，本地开发无需理会
2. 进入virtualenv，pip install -r requirements.txt
3. 修改config.py文件，本地开发直接使用sqlite(或修改配置文件中数据库账号密码)
4. 运行代码 python manage.py dev
