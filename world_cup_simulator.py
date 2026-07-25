# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم
# کلاس شبیه ساز جام جهانی

import csv           # برای خوندن فایل تیم‌ها که فرمتش csv هست
import os             # برای پیدا کردن و چک کردن وجود فایل csv
import random         # برای قرعه‌کشی سیدبندی لازمه

from team import Team               # هر تیم رو با این کلاس می‌سازیم
from match import Match             # بازی‌های گروهی و حذفی رو با این کلاس اجرا می‌کنیم
from group import Group             # هر گروه رو با این کلاس مدیریت می‌کنیم
from knockout_stage import KnockoutStage   # هر مرحله از فاز حذفی رو با این کلاس نگه می‌داریم

try:
    import matplotlib.pyplot as plt   # فقط برای رسم نمودار درصد قهرمانی در آخر کار، چیز ضروری‌ای نیست
    HAS_PLT = True                     # اگه نصب بود این پرچم true میشه و بعدا نمودار رو می‌کشیم
except ImportError:
    HAS_PLT = False                    # اگه matplotlib نصب نبود برنامه نباید کرش کنه، فقط نمودار رو رد می‌کنیم


class WorldCupSimulator:
    """کلاس اصلی برنامه، از بارگذاری فایل CSV تا مشخص شدن قهرمان همه چیز از اینجا مدیریت میشه."""

    def __init__(self):
        self.teams = []              # لیست ۳۲ تیم، تا وقتی فایل بارگذاری نشه خالیه
        self.groups = []             # لیست ۸ گروه، بعد از قرعه‌کشی پر میشه
        self.round_of_16 = None      # این چهار تا مرحله حذفی هستن، تا وقتی اجرا نشن None می‌مونن
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None         # قهرمان نهایی، تا آخر تورنمنت مشخص نمیشه

    def _find_csv_file(self, filename):
        # اول همون مسیری که کاربر داده رو امتحان می‌کنیم، شاید درست باشه و نیازی به گشتن نباشه
        if os.path.exists(filename):
            return filename
        here = os.path.dirname(os.path.abspath(__file__))   # پوشه‌ای که خود این فایل پایتون توشه
        same_folder = os.path.join(here, os.path.basename(filename))   # شاید فایل کنار خود برنامه باشه
        if os.path.exists(same_folder):
            return same_folder
        for root, _, files in os.walk(here):   # اگه بازم نبود، توی زیرپوشه‌های کنار برنامه هم می‌گردیم
            if os.path.basename(filename) in files:
                return os.path.join(root, os.path.basename(filename))
        return None   # هیچ جا پیدا نشد، دیگه کاری نمیشه کرد

    def load_teams_from_csv(self, filename):
        """فایل csv تیم‌ها رو خودش پیدا می‌کنه و از هر سطرش یه شیء Team می‌سازه."""
        found_path = self._find_csv_file(filename)   # قبل هر چیزی سعی می‌کنیم مسیر واقعی فایل رو پیدا کنیم
        if found_path is None:                          # اگه هیچ جا پیدا نشد دیگه معطلش نمی‌کنیم
            print(f"Error: file '{filename}' was not found.")
            return False
        try:
            teams = []                                     # لیست موقت، اگه یه جای وسط خطا داد لیست اصلی خراب نشه
            with open(found_path, encoding="utf-8") as f:    # این دفعه از مسیر واقعی که پیدا کردیم می‌خونیم
                for row in csv.DictReader(f):                 # هر سطر یه دیکشنری با کلیدهای همون سرستون‌هاست
                    teams.append(Team(row["name"].strip(), int(row["attack"]),
                                       int(row["defense"]), int(row["rank"])))   # عددها رو صریحا تبدیل می‌کنیم
            self.teams = teams   # حالا که همه چی بدون خطا خونده شد، لیست اصلی رو آپدیت می‌کنیم
            print(f"{len(self.teams)} teams loaded successfully from '{found_path}'.")
            return True
        except (ValueError, KeyError) as e:   # یعنی یا ستون اشتباه بود یا عددها قابل تبدیل نبودن
            print(f"Error: the CSV file has an invalid format ({e}).")
            return False

    def _need_teams(self):
        # این تابع رو قبل هر عملیاتی صدا می‌زنیم که مطمئن بشیم کاربر قبلش فایل رو بارگذاری کرده
        if not self.teams:
            print("Please load the teams first (menu option 1).")
            return False
        return True

    def _draw_groups(self):
        # قرعه‌کشی واقعی: اول تیم‌ها رو بر اساس رتبه فیفا مرتب می‌کنیم و چهار تا سید ۸ تایی می‌سازیم
        by_rank = sorted(self.teams, key=lambda t: t.rank)
        pots = [by_rank[0:8], by_rank[8:16], by_rank[16:24], by_rank[24:32]]   # سید یک تا چهار
        for pot in pots:
            random.shuffle(pot)   # ترتیب داخل هر سید تصادفی میشه تا قرعه‌کشی واقعی به نظر برسه

        names = ["A", "B", "C", "D", "E", "F", "G", "H"]   # هشت گروه جام جهانی
        group_teams = {n: [] for n in names}                 # هر گروه با یه لیست خالی شروع میشه
        for pot in pots:
            for idx, team in enumerate(pot):
                group_teams[names[idx]].append(team)   # تیم شماره idx از هر سید میره توی گروه شماره idx

        self.groups = [Group(n, group_teams[n]) for n in names]   # حالا اشیای Group واقعی رو می‌سازیم

    def groups_draw_and_seed(self):
        """قرعه‌کشی گروه‌ها رو انجام میده، هر گروه دقیقا یک تیم از هر سید داره."""
        if not self._need_teams():
            return False
        self._draw_groups()   # منطق واقعی قرعه‌کشی توی این تابع کمکیه
        print("Group draw completed based on FIFA seeding.")
        return True

    def stage_group_run(self):
        """همه بازی‌های مرحله گروهی رو اجرا می‌کنه و جدول هر گروه رو چاپ می‌کنه."""
        if not self._need_teams():
            return False
        if not self.groups:                                          # اگه هنوز قرعه‌کشی نشده بی‌فایده‌ست ادامه بدیم
            print("Please run the group draw first (menu option 2).")
            return False
        for g in self.groups:
            g.matches_all_play()   # اول همه بازی‌های همه گروه‌ها رو اجرا می‌کنیم
        for g in self.groups:
            g.display_table()      # بعد جدول‌ها رو یکی‌یکی چاپ می‌کنیم
        return True

    def bracket_knockout_setup(self):
        """براکت یک‌هشتم رو از روی نتیجه گروه‌ها می‌سازه، ترکیب بازی‌ها ثابت و از قبل مشخصه."""
        first, second = {}, {}   # اول و دوم هر گروه رو جدا نگه می‌داریم که ساخت جفت‌ها راحت‌تر باشه
        for g in self.groups:
            first[g.name], second[g.name] = g.advance_teams()   # از همون رتبه‌بندی نهایی گروه استفاده می‌کنیم

        # این ترکیب یه قانون ثابته و ربطی به قرعه‌کشی تصادفی نداره: صعودکننده اول هر گروه با نفر دوم گروه بعدی
        pairs = [
            (first["A"], second["B"]), (first["C"], second["D"]),   # A1 مقابل B2 و C1 مقابل D2
            (first["E"], second["F"]), (first["G"], second["H"]),     # همینطور E1-F2 و G1-H2
            (first["B"], second["A"]), (first["D"], second["C"]),     # نصف پایینی براکت برعکس بالایی
            (first["F"], second["E"]), (first["H"], second["G"]),
        ]
        matches = [Match(t1, t2, is_knockout=True) for t1, t2 in pairs]   # همه اینا بازی حذفی هستن
        self.round_of_16 = KnockoutStage("Round of 16", matches)

    def stage_knockout_run(self):
        """کل فاز حذفی از یک‌هشتم تا فینال رو پشت سر هم اجرا می‌کنه و قهرمان رو برمی‌گردونه."""
        self.round_of_16.round_play()             # اول یک‌هشتم رو اجرا می‌کنیم
        winners = self.round_of_16.winners_get()    # برنده‌هاش رو می‌گیریم که برن مرحله بعد

        self.quarterfinals = KnockoutStage(
            "Quarterfinals", [Match(winners[i], winners[i + 1], True) for i in range(0, 8, 2)]
        )   # هر دو برنده‌ی پشت سر هم با هم جفت میشن
        self.quarterfinals.round_play()
        winners = self.quarterfinals.winners_get()

        self.semifinals = KnockoutStage(
            "Semifinals", [Match(winners[i], winners[i + 1], True) for i in range(0, 4, 2)]
        )
        self.semifinals.round_play()
        winners = self.semifinals.winners_get()

        final_match = Match(winners[0], winners[1], is_knockout=True)   # فینال فقط یک بازیه بین دو برنده نیمه‌نهایی
        final_match.play()
        self.final = KnockoutStage("Final", [final_match])

        self.champion = final_match.winner   # برنده فینال همون قهرمان کل جام جهانیه
        return self.champion

    def _run_full_tournament(self):
        # این تابع کمکی یک دور کامل تورنمنت رو از صفر تا صد اجرا می‌کنه، هم برای اجرای عادی هم برای شبیه‌سازی چندباره
        for t in self.teams:
            t.reset_stats()      # آمار قبلی هر تیم پاک میشه که با دور جدید قاطی نشه
        self._draw_groups()      # هر بار یه قرعه‌کشی تازه انجام میشه
        for g in self.groups:
            g.matches_all_play()   # مرحله گروهی کامل اجرا میشه
        self.bracket_knockout_setup()   # براکت حذفی از روی همون نتیجه گروهی ساخته میشه
        return self.stage_knockout_run()   # و فاز حذفی هم اجرا میشه، قهرمان همینجا مشخص میشه

    def simulation_full_run(self):
        """یک بار کل جام جهانی رو (گروهی + حذفی) اجرا می‌کنه و نتیجه هر مرحله رو کامل چاپ می‌کنه."""
        if not self._need_teams():
            return None
        champion = self._run_full_tournament()   # کل منطق توی این تابع کمکی هست
        for g in self.groups:
            g.display_table()   # جدول نهایی هر گروه رو نشون میدیم
        for stage in (self.round_of_16, self.quarterfinals, self.semifinals, self.final):
            stage.results_display()   # نتیجه یک‌هشتم، یک‌چهارم، نیمه‌نهایی و فینال رو هم کامل نشون میدیم
        print(f"Champion: {champion.name}")             # و اسم قهرمان
        return champion

    def champion_likely_most(self, simulations_num=1000):
        """کل تورنمنت رو چند بار پشت سر هم اجرا می‌کنه تا ببینه هر تیم چند درصد قهرمان میشه."""
        if not self._need_teams():
            return None
        if simulations_num <= 0:                          # عدد منفی یا صفر اصلا معنی نداره
            print("Error: number of simulations must be a positive integer.")
            return None

        counts = {t.name: 0 for t in self.teams}   # شمارنده قهرمانی هر تیم، اول همه صفر
        for _ in range(simulations_num):
            champ = self._run_full_tournament()      # هر بار یه تورنمنت کامل و مستقل اجرا میشه
            counts[champ.name] += 1                    # قهرمان اون دور رو یدونه اضافه می‌کنیم

        percentages = {name: c / simulations_num * 100 for name, c in counts.items()}   # تبدیل تعداد به درصد
        percentages = dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))   # از زیاد به کم مرتب کن

        print(f"Simulation completed for {simulations_num} runs.")
        print("Championship percentage per team:")
        for name, pct in percentages.items():
            if pct > 0:                                    # تیم‌هایی که حتی یک بارم قهرمان نشدن رو چاپ نمی‌کنیم
                print(f"{name}: {pct:.1f}%")

        if HAS_PLT:
            self._plot_chart(percentages)   # اگه matplotlib بود یه نمودار هم می‌کشیم، وگرنه از این قسمت رد میشیم
        return percentages

    def _plot_chart(self, percentages, top_n=10):
        # فقط ۱۰ تیم برتر رو رسم می‌کنیم چون اگه هر ۳۲ تیم باشه نمودار خیلی شلوغ و بی‌خونا میشه
        top = list(percentages.items())[:top_n]
        plt.figure(figsize=(10, 6))                                  # اندازه شکل رو تعیین می‌کنیم
        plt.bar([x[0] for x in top], [x[1] for x in top], color="steelblue")   # نمودار میله‌ای ساده
        plt.ylabel("Championship Probability (%)")                    # برچسب محور عمودی
        plt.title("World Cup 2026 Championship Probability")           # عنوان کلی نمودار
        plt.xticks(rotation=45, ha="right")                            # اسم تیم‌ها رو کج می‌کنیم که روی هم نیفتن
        plt.tight_layout()                                              # فاصله‌ها رو خودکار مرتب می‌کنه
        plt.savefig("championship_probability.png")                     # نمودار رو به صورت عکس ذخیره می‌کنیم
        plt.close()                                                      # شکل رو می‌بندیم که حافظه آزاد بشه
        print("Chart saved as 'championship_probability.png'.")

    def bracket_display(self):
        """براکت کامل فاز حذفی مربوط به آخرین اجرای کامل رو نشون می‌ده."""
        if self.final is None:   # یعنی هنوز هیچ اجرای کاملی نداشتیم که نشونش بدیم
            print("Please run a full simulation first (menu option 4 or 5).")
            return False
        print("===== Knockout Bracket =====")
        for stage in (self.round_of_16, self.quarterfinals, self.semifinals, self.final):
            stage.results_display()   # هر مرحله نتایجش رو خودش چاپ می‌کنه
        print(f"Champion: {self.champion.name}")
        return True