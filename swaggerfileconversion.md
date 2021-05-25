# Structured Documents to Apply a swaggerfile to AWS API Gateway 
:india: :smiley:
![Image of SwaggerFile](https://alexdunndev.files.wordpress.com/2018/05/swagger-logo-horizontal.png?w=600)  ![Image of AWS APIGateway](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRggYroBxUMfU6Q2ggcThqSQEkV6dCg_bX7TxjJFoJI8VT9lEzNG7ZT0A8PNxmB614218M&usqp=CAU)

### <p5>The Following procedure is for develop or build a open API specified swagger file which can be easily integrated with AWS API Gateway to deploy a set of APIs according to our need. The Final swagger file which is specifically converted by a swagger convertion tool developed by us. The final converted API Gateway suitable swaggerfile is already **Descriptive**, **CORS Configured** & **Header Specific** by the tool. We just had to add the **Stage Variable URL** to add an extra layer of security in our deployment.</p5>

#### <h4><u>**Instruction to Deploy :**</u></h4>

* Import previous postman collection (.json) file in to postman.
* Add the new api with description, response and normalized structured postman collection a,d export it to previous file and overwrite.
* Convert the postman_collection.json file to a Open API specified Swagger File by using Swagmanmock.
    ```
        swagmanmock convert -i test.yaml qubecart-admin-postman-collection.json qubecart-admin.yaml
    ```
* Run a server at 5000 port by executing `swaggerConverter.py` file.
* Open Postman and Hit the API `0.0.0.0:5000/msqube/convertswagger/` with following request body
    Example of Request Body:    
    ```
        {
        "file":"D:/Kinnar Chowdhury/swagger_conversion_tool/Qubecart-Admin.yaml",
        "config_file":"D:/Kinnar Chowdhury/swagger_conversion_tool/config_file.yaml",
        "swagger_file":"AWS-APIintegrated-Qubecart-Admin"
        }
    ```

* Open the **`<AWS-APIintegrated-Qubecart-Admin.yaml>`** file and make some changes according to AWS API Gateway.
    **Mandatory** Changes:
    - Replace **'200':** using **200:**
    - Replace any http://**`<IP>`:`<port>`**/`<api>` using http://**${stageVariables.url}**/`<api>`/

* Open AWS API Gateway using user IAM User access. Select preferred API from the List.
    - Select option for **import API**
    - Choose the AWS API Gateway Integrated Swagger file (mentioned earlier)
    - Choose Endpoint Type **Edge Optimized**.
    - Opt-in for **Fail on warning**.
    - Import Mode **Overwrite** / **Merge** according to the need.
    - Now add a method (**get**) in the root resource "/" and specify http request, provide the following api and save it.
    ```
        http://${stageVariables.url}/ 
    ```
    - Finally choose Deploy API and select the stage, provide the description (**Mandatory**) and Deploy.

<p>&nbsp;</p>

> Now Your API is deployed to AWS API Gateway. You can hit the API to check.  

> Contact us for further references.
    >  @kincho94  kinnar.chowdhury@msqube.com ,
    > @HaranathB  haranah.basak@msqube.com ,
    > @sleepyowl06  sourav.mondal@msqube.com   

<p>&nbsp;</p>

> Document Consolidated by  `KINNAR CHOWDHURY, Software Developer`  under  `MSQUBE TECHNOLOGY SOLUTIONS PVT. LTD.`  company as on  `25th May,2021`.
![QUBECART](https://www.msqube.com/wp-content/uploads/2020/11/QC_Logo_500pxl-1.png) `Product Licensed & Registered Under` ![MSQube Technology Solutions Pvt. Ltd.](https://media-exp1.licdn.com/dms/image/C560BAQGnh6vxRglwOg/company-logo_200_200/0/1569092363489?e=2159024400&v=beta&t=gBG2VbNpyn2aDwybZRlpYxhbrFhcRWUEAL24G6-psZo)

> `Thank You. Enjoy It!`:smiley: :+1:
