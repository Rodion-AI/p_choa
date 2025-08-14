'''
agent Ask
'''
from api.core_and_router import Core


class Ask(Core):

    system_for_ask = '''
    Ты — великолепный сотрудник финансового отдела торговой компании 'Фэмили'. Компания 
    занимается реализацией одежды, игрушек и закусками. У тебя прекрасно
    получается определять нужно ли задавать уточняющие вопросы, а так же ты умеешь
    их задавать. \n\n

    Твоя основная задача - проследить чтобы все поля в таблице были заполнены. Тебе
    будет предоставлятся список сущностей: [дата, сумма, счет, контрагент, описание]. 
    Ознакомся с ним и там где «-», где отсутсутсвуют данные, задай вопросы для уточнения. \n\n

    Пожалуйста, не сообщай, что заполняешь список.
    '''

    model_for_ask = 'gpt-4.1-nano-2025-04-14'

    temperature_for_ask = 0

    verbose_for_ask = 0 

    # конструктор
    def __init__(self, note, client):
        self.note = note
        self.client = client

        super().__init__(
            system = self.system_for_ask,
            model = self.model_for_ask,
            temperature = self.temperature_for_ask,
            verbose = self.verbose_for_ask
        )

    # функция активатор
    async def activate(self):
        user_for_ask = f'''
        Пожалуйста, ознакомся со списком {self.note}. \n\n

        Давай действовать последовательно: \n
        Шаг 1: Есть ли в списке «-», иначе сразу закончи диалог. \n
        Шаг 2: Определяем недостающие сущности. \n
        Шаг 3: Формируем вопросы для уточнения. \n
        Шаг 4: Выводим только лишь вопрос(-ы) для уточнения. \n\n

        Пожалуйста, задай все вопрос(-ы) в одном сообщении.
        Ответ:
        '''

        messages = [
            {'role':'system', 'content':self.system},
            {'role':'user', 'content':user_for_ask}
        ]



        completion = await self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            temperature = self.temperature
        )

        answer = completion.choices[0].message.content

        if self.verbose:
            print('\n ask: \n', answer)

        return answer