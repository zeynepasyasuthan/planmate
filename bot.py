import discord
from discord.ext import commands
from config import TOKEN
from database import Database

db = Database()

DAYS = [
    ("monday", "Pazartesi"),
    ("tuesday", "Salı"),
    ("wednesday", "Çarşamba"),
    ("thursday", "Perşembe"),
    ("friday", "Cuma"),
    ("saturday", "Cumartesi"),
    ("sunday", "Pazar"),
]

CATEGORIES = [
    ("fun", "Eğlenceli", "😂"),
    ("relax", "Sakin", "😌"),
    ("active", "Hareketli", "🏃"),
    ("games", "Oyun", "🎮"),
    ("food", "Yemek", "🍔"),
    ("cafe", "Kafe", "☕"),
    ("outdoor", "Dış Mekan", "🌳"),
    ("creative", "Yaratıcı", "🎨"),
    ("movie", "Film / Dizi", "🎬"),
]

# 3 ÖNERİ ÜRET
def get_recommendations(user, day, budget, category):

    results = []

    people = db.find_people(
        user["id"],
        day,
        category
    )

    for person in people:

        if len(results) == 3:
            break

        common_budget = min(
            budget,
            person["budget"]
        )

        activity = db.find_group_activity(
            category,
            common_budget
        )

        if activity:

            results.append(
                f"👥 **{person['username']} ile {activity['name']}**\n"
                f"💰 {activity['price']} TL / kişi"
            )


    # Eksik kalanları solo tamamla
    if len(results) < 3:

        solos = db.find_solo(
            category,
            budget,
            3 - len(results)
        )

        for activity in solos:

            results.append(
                f"👤 **{activity['name']}**\n"
                f"💰 {activity['price']} TL"
            )

    return results[:3]

# KAYIT - BÜTÇE
class RegisterBudget(discord.ui.Modal, title="Bütçe"):

    budget = discord.ui.TextInput(
        label="Genel bütçen",
        placeholder="Örn: 100"
    )

    def __init__(self, days, interests):
        super().__init__()
        self.days = days
        self.interests = interests

    async def on_submit(self, interaction):

        try:
            budget = int(self.budget.value)
        except ValueError:
            await interaction.response.send_message(
                "Bütçe sayı olmalı.",
                ephemeral=True
            )
            return

        db.save_user(
            interaction.user.id,
            interaction.user.display_name,
            budget,
            self.days,
            self.interests
        )

        await interaction.response.send_message(
            "✅ Kayıt tamamlandı!",
            view=MainMenu(),
            ephemeral=True
        )


# =========================
# KAYIT - İLGİ
# =========================

class InterestSelect(discord.ui.Select):

    def __init__(self, days):

        self.days = days

        options = [
            discord.SelectOption(
                label=label,
                value=value,
                emoji=emoji
            )
            for value, label, emoji in CATEGORIES
        ]

        super().__init__(
            placeholder="Neler yapmayı seversin?",
            options=options,
            min_values=1,
            max_values=len(options)
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            RegisterBudget(
                self.days,
                list(self.values)
            )
        )


class InterestView(discord.ui.View):

    def __init__(self, days):
        super().__init__()
        self.add_item(
            InterestSelect(days)
        )


# =========================
# KAYIT - GÜNLER
# =========================

class DaySelect(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(
                label=label,
                value=value
            )
            for value, label in DAYS
        ]

        super().__init__(
            placeholder="Boş olduğun günleri seç",
            options=options,
            min_values=1,
            max_values=7
        )

    async def callback(self, interaction):

        await interaction.response.edit_message(
            content="🎯 Neler yapmayı seversin?",
            view=InterestView(
                list(self.values)
            )
        )


class DayView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(
            DaySelect()
        )


# =========================
# AKTİVİTE - KATEGORİ
# =========================

class ActivityCategory(discord.ui.Select):

    def __init__(self, day, budget):

        self.day = day
        self.budget = budget

        options = [
            discord.SelectOption(
                label=label,
                value=value,
                emoji=emoji
            )
            for value, label, emoji in CATEGORIES
        ]

        super().__init__(
            placeholder="Ne yapmak istiyorsun?",
            options=options
        )

    async def callback(self, interaction):

        user = db.get_user(
            interaction.user.id
        )

        results = get_recommendations(
            user,
            self.day,
            self.budget,
            self.values[0]
        )

        if not results:
            text = "😕 Uygun öneri bulamadım."
        else:
            text = (
                "🎉 **Sana 3 öneri:**\n\n"
                + "\n\n".join(results)
            )

        await interaction.response.edit_message(
            content=text,
            view=None
        )


class CategoryView(discord.ui.View):

    def __init__(self, day, budget):
        super().__init__()

        self.add_item(
            ActivityCategory(
                day,
                budget
            )
        )


# =========================
# AKTİVİTE - BÜTÇE
# =========================

class ActivityBudget(discord.ui.Modal, title="Bugünkü bütçe"):

    budget = discord.ui.TextInput(
        label="Maksimum bütçe",
        placeholder="Örn: 50"
    )

    def __init__(self, day):
        super().__init__()
        self.day = day

    async def on_submit(self, interaction):

        try:
            budget = int(self.budget.value)
        except ValueError:

            await interaction.response.send_message(
                "Bütçe sayı olmalı.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "🎯 Nasıl bir şey yapmak istiyorsun?",
            view=CategoryView(
                self.day,
                budget
            ),
            ephemeral=True
        )


# =========================
# AKTİVİTE - GÜN
# =========================

class ActivityDay(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(
                label=label,
                value=value
            )
            for value, label in DAYS
        ]

        super().__init__(
            placeholder="Hangi gün?",
            options=options
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            ActivityBudget(
                self.values[0]
            )
        )


class ActivityDayView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(
            ActivityDay()
        )


# =========================
# ANA MENÜ
# =========================

class MainMenu(discord.ui.View):

    @discord.ui.button(
        label="Aktivite Bul",
        emoji="🎯",
        style=discord.ButtonStyle.green
    )
    async def activity(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "📅 Hangi gün için plan arıyorsun?",
            view=ActivityDayView(),
            ephemeral=True
        )


# =========================
# KAYIT
# =========================

class RegisterView(discord.ui.View):

    @discord.ui.button(
        label="Kayıt Ol",
        emoji="📝",
        style=discord.ButtonStyle.green
    )
    async def register(
        self,
        interaction,
        button
    ):

        await interaction.response.edit_message(
            content="📅 Hangi günler boşsun?",
            view=DayView()
        )


# =========================
# BAŞLA
# =========================

class StartView(discord.ui.View):

    def __init__(self):
        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="Başla",
        emoji="▶️",
        style=discord.ButtonStyle.green,
        custom_id="planmate_start"
    )
    async def start(
        self,
        interaction,
        button
    ):

        user = db.get_user(
            interaction.user.id
        )

        if user is None:

            await interaction.response.send_message(
                "👋 Önce seni kaydedelim.",
                view=RegisterView(),
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                f"👋 Hoş geldin **{interaction.user.display_name}**!",
                view=MainMenu(),
                ephemeral=True
            )


# =========================
# BOT
# =========================

class PlanMate(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )

    async def setup_hook(self):

        db.setup()

        self.add_view(
            StartView()
        )

        await self.tree.sync()


bot = PlanMate()


# =========================
# /panel
# =========================

@bot.tree.command(
    name="panel",
    description="PlanMate panelini açar."
)
async def panel(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "🎉 **Bugün ne yapmak istersin?**\n"
        "Sana uygun aktiviteler ve kişiler bulabilirim.",
        view=StartView()
    )


@bot.event
async def on_ready():

    print(
        f"PlanMate aktif: {bot.user}"
    )


bot.run(TOKEN)