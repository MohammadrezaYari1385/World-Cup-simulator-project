# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم
# کلاس مسابقات
class Match:
    """یک بازی مشخص بین دو تیم، وظیفه اجرا کردنش و آپدیت آمار با اینجاست."""

    def __init__(self, team1, team2, is_knockout=False):
        self.team1 = team1              # تیم اول
        self.team2 = team2              # تیم دوم
        self.goals1 = 0                 # گل تیم اول، بعد از play() پر میشه
        self.goals2 = 0                 # گل تیم دوم
        self.is_knockout = is_knockout   # این پرچم تعیین می‌کنه که وقت اضافه و پنالتی حساب بشه یا نه
        self.winner = None               # فقط توی مرحله حذفی معنا داره، توی گروهی ممکنه None بمونه
        self.penalty_score = None        # اگه بازی به پنالتی رفت این مقدار پر میشه

    def play(self):
        """بازی رو واقعا اجرا می‌کنه، یعنی شبیه‌سازی می‌کنه و آمار دو طرف رو آپدیت می‌کنه."""
        g1, g2, winner, pens = self.team1.simulate_match(self.team2, self.is_knockout)   # نتیجه از دل تیم اول میاد
        self.goals1, self.goals2, self.winner, self.penalty_score = g1, g2, winner, pens   # همه چیز رو ذخیره می‌کنیم

        # گل‌های پنالتی جزو گل واقعی بازی حساب نمیشن، فقط برای مشخص کردن برنده استفاده شدن
        self.team1.for_goals += g1        # گل زده تیم اول
        self.team1.against_goals += g2    # گل خورده تیم اول
        self.team2.for_goals += g2        # گل زده تیم دوم
        self.team2.against_goals += g1    # گل خورده تیم دوم

        if not self.is_knockout:   # فقط توی مرحله گروهی امتیاز معنا داره، توی حذفی چیزی به امتیاز اضافه نمیشه
            if winner is self.team1:
                self.team1.points += 3   # برد یعنی ۳ امتیاز
            elif winner is self.team2:
                self.team2.points += 3   # همین برای تیم دوم
            else:
                self.team1.points += 1   # مساوی یعنی هر دو طرف ۱ امتیاز می‌گیرن
                self.team2.points += 1

    def result_string(self):
        """یه رشته خوانا از نتیجه بازی می‌سازه، برای چاپ توی خروجی و نمایش براکت."""
        text = f"{self.team1.name} {self.goals1}-{self.goals2} {self.team2.name}"   # نتیجه پایه بازی
        if self.penalty_score:                                                       # اگه پنالتی داشتیم
            text += f" ({self.penalty_score[0]}-{self.penalty_score[1]} pens)"        # نتیجه پنالتی رو اضافه کن
        if self.winner:                                                              # اگه برنده مشخص بود
            text += f" -> Winner: {self.winner.name}"                                 # اسمش رو هم بنویس
        return text   # این رشته همون چیزیه که موقع نمایش براکت چاپ میشه