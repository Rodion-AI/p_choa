from core_and_router import Core


class Analyze(Core):
    # прописываем роль, версию, температура модели
    system_for_analyze = '''
    Тебя зовут Пак Чхо А. Ты — великолепная сотрудница финансового отдела 
    торговой компании "Фэмили". Компания занимается реализацией одежды, 
    игрушек и закусками. Ты великолепный финансист в торговой компании, у тебя
    изумительно получается анализировать отчеты. Пожалуйста, будь внимательной
    и точной в цифрах.

    Тебе предоставлен отчет компании и тебе нужно сформулировать аналитическую записку
    для руководства компании. \n\n

    Ты знаешь что отчеты могут быть: \n
    - ОДДС или Отчет о движении денежных средств \n
    - ББ или Бухгалтерский баланс \n
    - ОПиУ или Отчет о прибыли и убытках. \n\n

    Твой ответ — только аналитическая записка, без технических пояснений.
    '''
    model_for_analyze = 'gpt-4.1-nano-2025-04-14'
    temperature_for_analyze = 0
    verbose_for_analyze = 0

    def __init__(self, sheet, client):
        self.sheet = sheet
        self.client = client

        super().__init__(
            system = self.system_for_analyze,
            model = self.model_for_analyze,
            temperature = self.temperature_for_analyze,
            verbose = self.verbose_for_analyze
        )

    async def activate(self):
        user_for_analyze = f'''
        Пожалуйста, давай действовать последовательно: \n
        Шаг 1: Определи вид предоставленного отчета. \n
        Шаг 2: Проанализируй отчет учитывая данные из Шаг 1. \n
        Шаг 3: Напиши аналитическую записку для руководства. \n\n

        Отвечай, пожалуйста, точно, и ничего не придумывай от себя.
        В ответе напиши **только аналитическую записку**, как если 
        бы ты писал её для руководителя. Не описывай шаги, не 
        объясняй ход работы. \n\n

        Предоставленный тебе отчет: {self.sheet}
        Ответ:
        '''

        messages = [
            {'role':'system', 'content':self.system},
            {'role':'user', 'content':user_for_analyze}
        ]

        completion = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            temperature = self.temperature
        )

        answer = completion.choices[0].message.content

        if self.verbose:
            print('\n analyze: \n', answer)

        return answer
