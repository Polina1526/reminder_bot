# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for an assistant that schedules reminders and
# reacts to external events.

from typing import Any, Text, Dict, List
import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet


# class ActionSetUsualReminder(Action):
#     """Schedules a reminder, supplied with the last message's entities."""
#
#     def name(self) -> Text:
#         return "action_set_usual_reminder"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text = "I will remind you in 5 seconds.")
#
#         # date = datetime.datetime.now() + datetime.timedelta(seconds=5)
#         date = datetime.datetime.now() + datetime.timedelta(minutes=5)
#
#         entities = tracker.latest_message.get("entities")
#
#         reminder = ReminderScheduled(
#             "EXTERNAL_reminder",
#             trigger_date_time=date,
#             entities=entities,
#             name="my_reminder",
#             kill_on_user_message=False,
#         )
#
#         return [reminder]


# class ActionSetCallReminder(Action):
#     """Schedules a reminder, supplied with the last message's entities."""
#
#     def name(self) -> Text:
#         return "action_set_call_reminder"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text = "I will remind you to call in 5 seconds.")
#
#         date = datetime.datetime.now() + datetime.timedelta(seconds=5)
#         entities = tracker.latest_message.get("entities")
#
#         reminder = ReminderScheduled(
#             "EXTERNAL_reminder",
#             trigger_date_time=date,
#             entities=entities,
#             name="my_reminder",
#             kill_on_user_message=False,
#         )
#
#         return [reminder]


class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = next(tracker.get_slot("PERSON"), "someone")
        dispatcher.utter_message(f"Remember to call {name}!")

        return []


class ActionTellID(Action):
    """Informs the user about the conversation ID."""

    def name(self) -> Text:
        return "action_tell_id"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id = tracker.sender_id

        dispatcher.utter_message(f"The ID of this conversation is '{conversation_id}'.")
        dispatcher.utter_message(
            f"Trigger an intent with: \n"
            f'curl -H "Content-Type: application/json" '
            f'-X POST -d \'{{"name": "EXTERNAL_dry_plant", '
            f'"entities": {{"plant": "Orchid"}}}}\' '
            f'"http://localhost:5005/conversations/{conversation_id}'
            f'/trigger_intent?output_channel=latest"'
        )

        return []


class ActionWarnDry(Action):
    """Informs the user that a plant needs water."""

    def name(self) -> Text:
        return "action_warn_dry"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        plant = next(tracker.get_latest_entity_values("plant"), "someone")
        dispatcher.utter_message(f"Your {plant} needs some water!")

        return []


class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Okay, I'll cancel all your reminders.")

        # Cancel all reminders
        return [ReminderCancelled()]


class DefaultFallback(Action):
    """React to unknown frase"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response = "utter_default_fallback")

        return []


class UsualReminderForm(FormAction):
    """Custom form action to fill all slots required to remind the user to do something"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "usual_reminder_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["txt_reminder", "timer"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"txt_reminder": self.from_entity(entity="txt_reminder",
                                                 intent=["ask_usual_reminder"]),
                "timer": self.from_entity(entity="timer",
                                          intent=["ask_usual_reminder"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, set the reminder"""

        txt_reminder = tracker.get_slot('txt_reminder')
        timer = tracker.get_slot('timer')

        # dispatcher.utter_message(response = "utter_default_fallback")

        dispatcher.utter_message(text="I will remind you to do '{}' in {} minutes.".format(txt_reminder, timer))

        date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        # entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return []


class CallReminderForm(FormAction):
    """Custom form action to fill all slots required to remind the user to call to somebody"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "call_reminder_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["person", "timer"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"person": self.from_entity(entity="person",
                                           intent=["ask_call_reminder"]),
                "timer": self.from_entity(entity="timer",
                                          intent=["ask_call_reminder"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, set the reminder"""

        person = tracker.get_slot('person')
        timer = tracker.get_slot('timer')

        # dispatcher.utter_message(response = "utter_default_fallback")

        dispatcher.utter_message(text="I will remind you to call '{}' in {} minutes.".format(person, timer))

        date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        # entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return []
