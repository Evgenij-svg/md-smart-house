#include <WiFi.h>
#include <ESPAsyncWebServer.h>

#define PWMB 5
#define BIN1 19
#define BIN2 18


// Пример переменной, значение которой будет выводиться на веб-страницу
String sensorValue = " ";

String SensorPrev = " ";

// const char* ssid = "TechnoPark";
// const char* password = "test@TEST";

// const char* ssid = "mdwifi";
// const char* password = "12345678";

const char* ssid = "obshc_tehnop";
const char* password = "0123456789";

// Создаем объект сервера на порту 80
AsyncWebServer server(80);

const int Kuler = 14;
const int Vent = 26;
const int relay = 27;
bool StateModeGesturesBool[3] = { false, false, false };
byte brightness = 100;

void handleChangeVariable(AsyncWebServerRequest* request) {
  // Получаем параметры запроса
  String name = request->getParam("name")->value();
  String value = request->getParam("value")->value();

  // Изменяем значение переменной
  if (name == "myVariable") {
    Serial.println(value);
    brightness = value.toInt();
  }
  if (name == "rele1") {
    StateModeGesturesBool[0] = !StateModeGesturesBool[0];
  }
  if (name == "rele2") {
    StateModeGesturesBool[1] = !StateModeGesturesBool[1];
  }
  if (name == "rele3") {
    StateModeGesturesBool[2] = !StateModeGesturesBool[2];
  }


  // Отправляем ответ клиенту
  request->send(200, "text/plain", "OK");
}


void setup() {
  pinMode(Kuler, OUTPUT);
  pinMode(Vent, OUTPUT);
  pinMode(relay, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  Serial.begin(115200);
  delay(1000);
  Serial.println();
  Serial.print("Подключение к Wi-Fi...");
  WiFi.begin(ssid, password);  // Подключение к существующей сети Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Подключение к Wi-Fi выполнено успешно!");
  Serial.print("IP-адрес ESP32: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest* request) {
    // Формируем HTML-страницу с использованием JavaScript для обновления значения переменной
    String html = "<html> <head><meta charset='utf-8'><title>Умный дом</title></head><body>";
    html += "<h1>My Varrible: <span id='sensorValue'></span></h1>";
    html += "<input type=\"checkbox\" onclick=\"changeVariable('rele1', ' ');\" class='Ceckbox1'>rele1</input>";
    html += "<input type=\"checkbox\" onclick=\"changeVariable('rele2', ' ');\" class='Ceckbox2'>rele2</input>";
    html += "<input type=\"checkbox\" onclick=\"changeVariable('rele3', ' ');\" class='Ceckbox3'>rele3</input>";
    html += "<div> <button onclick =\"getLenta('More');\">Больше +25</button><span class= 'Lenta'> 120 </span> <button onclick =\"getLenta('Less');\">Меньше -25</button></div> ";
    html += "<script>var sensorValue = document.getElementById('sensorValue');";
    html += "const Lenta = document.querySelector('.Lenta'); let brightness = 100; let prevbrightness = 120; function getLenta(value) { if (value == 'Less') { if(brightness == 0){brightness = 0;}else{brightness = brightness - 25;} } if (value == 'More') { if(brightness == 250){brightness=250}else{brightness = parseInt(brightness)+25;} } Lenta.innerText = brightness; changeVariable('myVariable', brightness); }";
    html += "setInterval(function() {";
    html += "fetch('/sensor').then(response => response.text()).then(data => {";
    html += " let arr = data.split(' '); if(!arr[0]){arr[0]='noGestures';} const filteredArr = arr.filter(function(str) {return str.trim() !== '';}); brightness = filteredArr[1];if(prevbrightness  !=  brightness){Lenta.innerText = brightness;} prevbrightness=brightness; sensorValue.innerText =filteredArr[0]; document.querySelector('.Ceckbox1').checked=Boolean(parseInt(filteredArr[2]));document.querySelector('.Ceckbox2').checked=Boolean(parseInt(filteredArr[3])); ";
    html += "document.querySelector('.Ceckbox3').checked=Boolean(parseInt(filteredArr[4]));";
    //html += "sensorValue.textContent = data; let arr = data.toString().spllit(' ');";
    html += "});";
    html += "}, 300);";
    html += "function changeVariable(variableName, variableValue) {";
    html += "var xhr = new XMLHttpRequest();";
    html += "xhr.open('GET', '/changeVariable?name=' + variableName + '&value=' + variableValue);";  // Отправляем GET-запрос на /changeVariable с параметрами name и value
    html += "xhr.send();";
    html += "}";
    html += "</script>";
    html += "</body></html>";
    request->send(200, "text/html", html);
  });

  server.on("/changeVariable", HTTP_GET, handleChangeVariable);

  // Обработчик маршрута для получения значения переменной
  server.on("/sensor", HTTP_GET, [](AsyncWebServerRequest* request) {
    // Отправляем значение переменной в ответ на запрос
    String stateStr = "";
    for (int i = 0; i < 3; i++) {
      stateStr = stateStr + StateModeGesturesBool[i] + " ";
    }
    request->send(200, "text/plain", sensorValue + " " + brightness + " " + stateStr);
  });

  server.on("/data", HTTP_POST, [](AsyncWebServerRequest* request) {
    String data = request->arg("gestures");


      sensorValue = data;
      sensorValue = removeBeforeLastSpace(sensorValue);
      Serial.print("Получено: ");
      Serial.println(sensorValue);      
    

    if (sensorValue == "Victory" && sensorValue != SensorPrev) {
      StateModeGesturesBool[0] = !StateModeGesturesBool[0];
    }
    if (sensorValue == "OK" && sensorValue != SensorPrev) {
      StateModeGesturesBool[1] = !StateModeGesturesBool[1];
    }
    if (sensorValue == "Up" && sensorValue != SensorPrev) {
      StateModeGesturesBool[2] = !StateModeGesturesBool[2];
    }
    if (sensorValue == "left" && sensorValue != SensorPrev) {
      if (brightness == 0) {
        brightness = 0;
      } else {
        brightness = brightness - 25;
      }
    }
    if (sensorValue == "right" && sensorValue != SensorPrev) {
      if (brightness == 250) {
        brightness = 250;
      } else {
        brightness = brightness + 25;
      }
    }
    SensorPrev = sensorValue;
    request->send(200, "text/plain", "data received");
  });

  // Запуск сервера
  server.begin();
}

String removeBeforeLastSpace(String inputString) {
  int spaceIndex = inputString.lastIndexOf(' ');   // Ищем индекс последнего пробела
  if (spaceIndex != -1) {                          // Если пробел найден
    return inputString.substring(spaceIndex + 1);  // Возвращаем подстроку после пробела
  } else {
    return inputString;  // Если пробел не найден, возвращаем исходную строку
  }
}



void loop() {
  if (Serial.available() > 0) {                  // Проверяем, есть ли данные в буфере последовательного порта
    sensorValue = Serial.readStringUntil('\n');  // Читаем строку до символа перевода строки
    sensorValue = removeBeforeLastSpace(sensorValue);
  }
  if (sensorValue == "Victory" && sensorValue != SensorPrev) {
    StateModeGesturesBool[0] = !StateModeGesturesBool[0];
    Serial.println(StateModeGesturesBool[0]);
  }
  if (sensorValue == "OK" && sensorValue != SensorPrev) {
    StateModeGesturesBool[1] = !StateModeGesturesBool[1];
    Serial.println(StateModeGesturesBool[1]);
  }
  if (sensorValue == "Up" && sensorValue != SensorPrev) {
    StateModeGesturesBool[2] = !StateModeGesturesBool[2];
    Serial.println(StateModeGesturesBool[2]);
  }
  if (sensorValue == "left" && sensorValue != SensorPrev) {
    if (brightness == 0) {
      brightness = 0;
    } else {
      brightness = brightness - 25;
    }
  }
  if (sensorValue == "right" && sensorValue != SensorPrev) {
    if (brightness == 250) {
      brightness = 250;
    } else {
      brightness = brightness + 25;
    }
  }
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
  analogWrite(PWMB, brightness);
  SensorPrev = sensorValue;
  digitalWrite(Kuler, StateModeGesturesBool[0]);
  digitalWrite(Vent, StateModeGesturesBool[1]);
  digitalWrite(relay, StateModeGesturesBool[2]);
}