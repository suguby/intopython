# -*- coding: utf-8 -*-
import random

from django.core.management import BaseCommand

from src.blog.models import Blog
from src.screencasts.models import ScreencastSection, Screencast


class DbFiller:

    TITLES = (
        'Как я борол Эксель',
        'Установка PyCharm',
        'Деплой Django',
        'Как установить пайтон? Ну, не знаю...',
        'Django ORM и его особенности',
        'Применение bash в программировании',
        'Наконец-то вышел новый Django! Посмотрим что у него внутри ',
    )

    SUMMARIES = (
"""Силовое поле просветляет плазменный осциллятор. Субаренда переворачивает широкий фотон.
Если в соответствии с законом допускается самозащита права, нижнее течение бифокально берёт городской экситон.
Страховая сумма существенно отталкивает лазер. Новация надкусывает протяженный гарант как при нагреве, так и при охлаждении.
""",
"""
Бытовой подряд, куда входят Пик-Дистрикт, Сноудония и другие многочисленные
национальные резерваты природы и парки, анонимно отражает обычай делового оборота.
Помимо права собственности и иных вещных прав, ограниченная ответственность иллюстрирует электрон.
Коневодство отталкивает штраф, при этом дефект массы не образуется.
""",
"""
Возмущение плотности стабилизирует взаимозачет. Скумбрия, на первый взгляд, поднимает субъект.
Когда из храма с шумом выбегают мужчины в костюмах демонов и смешиваются с толпой, двухпалатный парламент квантуем.
Аккредитив, по данным астрономических наблюдений, переворачивает коносамент.

Высотная поясность надкусывает урбанистический снежный покров, при этом разрешен провоз
3 бутылок крепких спиртных напитков, 2 бутылок вина; 1 л духов в откупоренных флаконах,
2 л одеколона в откупоренных флаконах. Преамбула точно отталкивает живописный взаимозачет.

Отгонное животноводство бесконтрольно нейтрализует протяженный обычай делового оборота.
Перестрахование по определению субъективно отражает Указ в том случае, когда процессы переизлучения спонтанны.
Разрыв изменяем.
""",
    )

    TEXTS = (
"""
Ретардация отражает индивидуальный гомеостаз. Самонаблюдение решает эллиптический аутизм.
Красноватая звездочка, иcходя из того, что непоследовательно отражает далекий гештальт.
""",
"""
Когда речь идет о галактиках, восприятие выбирает депрессивный комплекс.
Расстояния планет от Солнца возрастают приблизительно в геометрической прогрессии
(правило Тициуса — Боде): г = 0,4 + 0,3 · 2n (а.е.), где роль вероятна. `cat /ets/passwd`

Этот концепт элиминирует концепт «нормального», однако керн выбирает
экваториальный экватор. Летучая Рыба, несмотря на внешние воздействия,
вызывает узел. Самонаблюдение оценивает болид. Обязательство устойчиво нейтрализует ускоряющийся акцепт.
Сингулярность вознаграждает платежный документ, но особой популярностью пользуются заведения подобного рода,
сосредоточенные в районе Центральной площади и железнодорожного вокзала.
Новая Гвинея восстанавливает товарный кредит. Линза просветляет императивный солитон.
""",
"""
Кульминация отталкивает психоанализ, хотя для имеющих глаза-телескопы туманность Андромеды
показалась бы на небе величиной с треть ковша Большой Медведицы. Мышление, как бы это ни казалось парадоксальным,
однородно вызывает филогенез. Астероид отражает оппортунический Южный Треугольник,
о чем и писал А.Маслоу в своей работе "Мотивация и личность"

Доминантсептаккорд добросовестно использует акцепт. Полимодальная организация реквизирует шоу-бизнес,
в таких условиях можно спокойно выпускать пластинки раз в три года. Концессия противозаконна.

    def run(self):
        if self.options.get('clear', False):
            self._clean_db()
        self.question_count = self.anwsers_count = 0
        self.organisation, created = Organisation.objects.get_or_create(name='Икеа', slug='ikea')
        self.presentations = self._get_presentations()
        print('Added {} presentations'.format(len(self.presentations)))
        self.slides = self._get_slides()
        print('Added {} slides'.format(len(self.slides)))
        self._append_questions()
        print('Added {} questions with {} anwsers'.format(self.question_count, self.anwsers_count))


Индоссамент опротестован. В соответствии со сложившейся правоприменительной практикой конфиденциальность
синхронно гарантирует гарантийный субъект. Звукосниматель объективно добросовестно использует ничтожный цикл.
Банкротство гарантирует конфиденциальный канал. Аллюзийно-полистилистическая композиция принципиально
экспортирует open-air. Фрахтование формирует доминантсептаккорд. Ретро имитирует соноропериод.

Адажио деформирует причиненный ущерб. Разлом страхует причиненный ущерб, включая и гряды Чернова, Чернышева и др.
Из комментариев экспертов, анализирующих законопроект, не всегда можно определить, когда именно океаническое ложе
обогащает апериодический предпринимательский риск. Арпеджио поручает конструктивный шельф, это и есть одномоментная
вертикаль в сверхмногоголосной полифонической ткани. Согласно теории устойчивости движения авгит позволяет
пренебречь колебаниями корпуса, хотя этого в любом случае требует биокосный экваториальный момент.
Тальвег, в первом приближении, дает меандр, что не имеет аналогов в англо-саксонской правовой системе.
Исключая малые величины из уравнений, погрешность относительно лицензирует флэнжер. Момент сил неустойчив.
Внутреннее кольцо позволяет исключить из рассмотрения пелагический гарант. Наследование последовательно.
Помимо права собственности и иных вещных прав, Указ своевременно исполняет цокольный субъект.

Рефрен утолщен. Кластерное вибрато поступательно. В соответствии с законами сохранения энергии,
гипергенный минерал анизотропно формирует уходящий товарный кредит, за счет чего увеличивается мощность коры
под многими хребтами. Несомненный интерес представляет и тот факт, что гипнотический рифф вызывает жидкий акцепт.
В самом общем случае магма отчетливо и полно арендует огненный пояс. Цикл использует оз.
При наступлении резонанса поверхность представляет собой изобарический страховой полис, что в переводе означает
"город ангелов". Частица, в отличие от классического случая, жизненно входит тангенциальный сверхпроводник.
Преступление формирует урбанистический склон Гиндукуша, несмотря на то, что все здесь

выстроено в оригинальном славянско-турецком стиле. Химическое соединение, как следует из совокупности экспериментальных наблюдений,
недееспособно. Взаимозачет, при адиабатическом изменении параметров, декларирует шведский вечнозеленый
кустарник, хотя этот факт нуждается в дальнейшей тщательной экспериментальной проверке.
Погранслой доказывает ледостав, исключая принцип презумпции невиновности.

Законодательство поднимает попугай. В ряде недавних экспериментов Гвианский щит виновно декларирует суд.
Судебное решение мгновенно экспортирует экситон. Бытовой подряд, вследствие публичности данных отношений,
наследует короткоживущий Указ. Гомогенная среда применяет страховой полис, хотя все знают, что Венгрия
подарила миру таких великих композиторов как Ференц Лист, Бела Барток, Золтан Кодай, режиссеров Иштвана Сабо
и Миклоша Янчо, поэта Шандора Пэтефи и художника Чонтвари. При приватизации имущественного комплекса аналогия
закона едва ли квантуема.
""",
)
    VIDEOS = (
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/9sbFZi2lpdY" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="420" height="315" src="https://www.youtube.com/embed/bGsnwowAfRw" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/B1sjE2_B_40" frameborder="0" allowfullscreen></iframe>',
    )
    SECTIONS = ('Django', 'Python', 'PyCharm', 'Deploy', )
    TAGS = (
        'collaborators',
        'django',
        'fractals',
        'githib',
        'issues',
        'lessons',
        'ORM',
        'pep8',
        'pycharm',
        'python',
        'recursion',
        'regex',
        'virtualenv',
    )

    def __init__(self, options):
        self.options = options
        self.sections = None
        self.screencasts = None

    def _get_option_range(self, name, default='3-5'):
        params = self.options.get(name, default).split('-')
        try:
            a, b = params
        except ValueError:
            a = b = params[0]
        return range(random.randint(int(a), int(b)))

    def run(self):
        if self.options.get('clear', False):
            self._clean_db()
        self.sections = self._get_sections()
        print('Added {} sections'.format(len(self.sections)))
        self.screencasts = self._get_screencasts()
        print('Added {} screencasts'.format(len(self.screencasts)))
        self.blogs = self._get_blogs()
        print('Added {} blogs'.format(len(self.blogs)))

    def _get_sections(self):
        sections = []
        for i in self._get_option_range('sections'):
            title = random.choice(self.SECTIONS)
            section, created = ScreencastSection.objects.get_or_create(
                title=title,
                defaults=dict(
                    slug=title.lower(),
                    position=i,
                    status=ScreencastSection.STATUSES.publ,
                )
            )
            sections.append(section)
        return sections

    def _get_screencasts(self):
        screencasts = []
        for i in self._get_option_range('screencasts'):
            title = random.choice(self.TITLES)
            sc, created = Screencast.objects.get_or_create(
                title=title,
                type=Screencast.TYPES.screencast,
                defaults=dict(
                    video=random.choice(self.VIDEOS),
                    section=random.choice(self.sections),

                    summary=random.choice(self.SUMMARIES),
                    body=random.choice(self.TEXTS),
                    status=ScreencastSection.STATUSES.publ,
                    by_subscription=random.choice([True, False]),
                )
            )
            sc.tags.set(*self._get_tags())
            screencasts.append(sc)
        return screencasts

    def _get_tags(self):
        return [random.choice(self.TAGS) for i in self._get_option_range('tags')]

    def _get_blogs(self):
        blogs = []
        for i in self._get_option_range('blogs'):
            title = random.choice(self.TITLES)
            bl, created = Blog.objects.get_or_create(
                title=title,
                type=Screencast.TYPES.blog,
                defaults=dict(
                    summary=random.choice(self.SUMMARIES),
                    body=random.choice(self.TEXTS),
                    status=ScreencastSection.STATUSES.publ,
                    by_subscription=random.choice([True, False]),
                )
            )
            bl.tags.set(*self._get_tags())
            blogs.append(bl)
        return blogs

    def _clean_db(self):
        Blog.objects.all().delete()
        Screencast.objects.all().delete()
        ScreencastSection.objects.all().delete()
        print('Database cleaned')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--clear',
                            action='store_true',
                            dest='clear',
                            default=False,
                            help='очистить предварительно базу')
        parser.add_argument('--sections',
                            action='store',
                            dest='sections',
                            default='3-5',
                            help='сколько создавать секций (можно диапазоном)')
        parser.add_argument('--screencasts',
                            action='store',
                            dest='screencasts',
                            default='5-10',
                            help='сколько создавать скринкастов (можно диапазоном)')
        parser.add_argument('--blogs',
                            action='store',
                            dest='blogs',
                            default='5-10',
                            help='сколько создавать записей блога (можно диапазоном)')

    def handle(self, *args, **options):
        runner = DbFiller(options=options)
        runner.run()
