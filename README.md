Описание моей работы смотри в конце README.md
# Reminderbot

The `reminderbot` example demonstrates how your bot can respond to external events or reminders.

## What’s inside this example?

This example contains some training data and the main files needed to build an
assistant on your local machine. The `reminderbot` consists of the following files:

- **data/nlu.yml** contains training examples for the NLU model
- **data/rules.yml** contains rules for the Core model
- **config.yml** contains the model configuration
- **domain.yml** contains the domain of the assistant
- **credentials.yml** contains credentials for the different channels
- **endpoints.yml** contains the different endpoints reminderbot can use
- **actions/actions.py** contains the custom actions that deal with external events and reminders

## How to use this example?

To train and chat with `reminderbot`, execute the following steps:

1. Train a Rasa Open Source model containing the Rasa NLU and Rasa Core models by running:
    ```
    rasa train
    ```
    The model will be stored in the `/models` directory as a zipped file.

2. Run a Rasa SDK action server with
    ```
    rasa run actions
    ```

3. (Option 1) Run Rasa X to talk to your bot. In a separate console window from where you ran the step 2 command:
    ```
    rasa x
    ```

3. (Option 2) To test this example without Rasa X, run a
   [callback channel](https://rasa.com/docs/rasa/connectors/your-own-website#callbackinput).
   In a separate console window from where you ran the step 2 command:
    ```
    python callback_server.py
    ```

   This will run a server that prints the bot's responses to the console.

   Start your Rasa server in a third console window:
   ```
   rasa run --enable-api
   ```

   You can then send messages to the bot via the callback channel endpoint:
   ```
   curl -XPOST http://localhost:5005/webhooks/callback/webhook \
      -d '{"sender": "tester", "message": "hello"}' \
      -H "Content-type: application/json"
   ```

For more information about the individual commands, please check out our
[documentation](http://rasa.com/docs/rasa/command-line-interface).

## Encountered any issues?
Let us know about it by posting on [Rasa Community Forum](https://forum.rasa.com)!



## Индивидуальное задание в рамках Raiffeisen Evolve 2022
Для выполнения задания я выбрала бота, который помогает пользователю устанавливать уведомления. Данный бот был представлен в качестве примернов в репозитории https://github.com/RasaHQ/rasa. Мне показалась интересной реализации подобного бота именно поэтому я остановилась на этом примере для улучшения. Изначально, бот был просто маленьким примером использования напоминаний в RASA и имел очень скудную реализацию.

Изменения, которые были внесены в Reminderbot:
1) Я решила разделить напоминания на два типа: обычное напоминание, которое может содержать любую информацию и нопоминание позвонить какому-то человеку. Для этого я определила две различные intentions и увеличила колличество тренировочных примеров в файле nlu.md для того, чтобы бот мог эффективно различать две этих intentions. Кроме того, я ввела несколько entities, необходимых для реализации двух вышеупомянутых intentions. Эти entities так же были представленны в тренировочных данных для того чтобы бот научился извлекать entities из сообщений пользователя. Это дало хороший результат и на экспериметах бот показывал достаточно высокий уровень confidance при извлечении данных entities.
2) Далее я кардинально изменила Policies, так как изначально в Reminderbot была использована только лишь RulePolicy и реализованны некоторые патерны. Это показалось мне странным, поэтому я скоректировала эту часть бота добавив иные Policies и подобрала некоторые гиперпараметры для них, это можно увидеть в файле config.yml.
3) Далее я занялась реализацией слотов и форм для того чтобы несколько изменить подход бота к установке уведомлений. Во-первых до этого бот принимал любое уведомление и ставил напоминание через 5 секунд. Введённые мною entities, слоты и формы дают возможность устанавливать уведомление через определённое количество минут, заданное пользователем. А сами уведомления перестали быть просто одинаковым предложением, а стали отображать содержание напоминания, которое задал пользователь (это относится к обычным уведомлениям). А для уведомлений о телефонном звонке теперь выдаётся сообщение о том, котому пользователь планировал совершить этот звонок.
4) Так же, для того чтобы бот мог хорошо обучиться патернам разговора с пользователям я добавила Stories, содержащие в себе патерны заполнения описанных выше форм.

Таким образом, бот стал гораздо более функциональным и разумным, чем когда был представлен в качестве примера изначально. Конечно, он ещё далёк от совершенства и от встречи с реальным пользователем, но тем не менее теперь Reminderbot уже имеет некоторую полезныю функциональность.
