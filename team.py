# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم
# کلاس تیم ها

import random         # برای شبیه‌سازی ضربات پنالتی لازمه
import numpy as np    # گل هر بازی رو با توزیع پواسون از اینجا می‌گیریم، هم سریع‌تره هم واقعی‌تر از یه عدد تصادفی ساده


class Team:
    """کلاس یک تیم ملی، هم مشخصاتش رو نگه می‌داره هم منطق شبیه‌سازی بازی‌هاشه."""

    def __init__(self, name, attack, defense, rank):
        self.name = name                # اسم تیم رو همینجوری خام ذخیره می‌کنیم
        self.attack = attack            # قدرت حمله، هرچی بیشتر باشه احتمال گل زدنش بالاتر میره
        self.defense = defense          # قدرت دفاع، توی فرمول گل حریف استفاده میشه نه گل خودش
        self.rank = rank                # رتبه فیفا، فقط برای سیدبندی موقع قرعه‌کشی لازممون میشه
        self.for_goals = 0              # جمع گل‌هایی که این تیم توی کل تورنمنت زده
        self.against_goals = 0          # جمع گل‌هایی که خورده، این دوتا با هم تفاضل گل رو میسازن
        self.points = 0                 # امتیاز مرحله گروهی، توی فاز حذفی اصلا استفاده نمیشه
        self.group = None               # اسم گروهش، بعد از قرعه‌کشی پر میشه (فقط جنبه اطلاعاتی داره)

    def goal_difference(self):
        """تفاضل گل، یکی از معیارهای رتبه‌بندی گروهه."""
        return self.for_goals - self.against_goals   # گل زده منهای گل خورده، همین ساده

    def reset_stats(self):
        """قبل از هر دور جدید شبیه‌سازی باید آمار قبلی رو پاک کنیم."""
        self.for_goals = 0        # وگرنه گل‌های دور قبل با دور جدید قاطی میشد
        self.against_goals = 0    # همینطور اینم صفر میشه
        self.points = 0           # امتیاز هم از نو شروع میشه

    def _lambda_vs(self, opponent):
        # این فرمول میانگین گل موردانتظار (لامبدای پواسون) رو حساب می‌کنه: هم حمله خودمون مهمه هم ضعف دفاع حریف
        lam = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        return max(lam, 0.01)   # لامبدای صفر یا منفی معنی نداره، پس یه حداقل خیلی کوچیک می‌ذاریم

    def _penalty_prob(self, opponent):
        # احتمال گل شدن هر پنالتی، هرچی حمله خودمون بیشتر و دفاع حریف کمتر باشه شانس گل بیشتره
        prob = 0.75 + (self.attack - opponent.defense) / 250
        return max(0.6, min(0.9, prob))   # این عدد نباید خیلی کم یا خیلی زیاد بشه، بین ۰.۶ تا ۰.۹ نگهش می‌داریم

    def penalty_shootout(self, opponent):
        """۵ پنالتی برای هر تیم می‌زنیم و اگه بازم مساوی بود میریم سراغ پنالتی ناگهانی."""
        p_self = self._penalty_prob(opponent)          # احتمال گل شدن پنالتی‌های خودمون
        p_opp = opponent._penalty_prob(self)             # احتمال گل شدن پنالتی‌های حریف
        goals_self = sum(1 for _ in range(5) if random.random() < p_self)  # ۵ ضربه رو شبیه‌سازی می‌کنیم
        goals_opp = sum(1 for _ in range(5) if random.random() < p_opp)     # همین کار رو برای حریف انجام میدیم

        while goals_self == goals_opp:              # اگه بعد ۵ ضربه مساوی بودن میریم توی حالت ناگهانی
            hit_self = random.random() < p_self       # یه ضربه‌ی جدید برای خودمون
            hit_opp = random.random() < p_opp          # یه ضربه‌ی جدید برای حریف
            if hit_self and not hit_opp:                # اگه فقط خودمون گل زدیم بازی همینجا تموم میشه
                goals_self += 1
                break
            if hit_opp and not hit_self:                # اگه فقط حریف گل زد اونم برنده میشه
                goals_opp += 1
                break
            # اگه هردو گل زدن یا هردو از دست دادن، یه دور دیگه امتحان می‌کنیم تا یکی جلو بیفته

        winner = self if goals_self > goals_opp else opponent   # حالا مقایسه ساده‌ی تعداد گل پنالتی
        return goals_self, goals_opp, winner   # این سه‌تا رو برمی‌گردونیم که توی نمایش نتیجه لازممون میشه

    def simulate_match(self, opponent, is_knockout=False):
        """یک بازی کامل رو شبیه‌سازی می‌کنه و گل خودی، گل حریف، برنده و نتیجه پنالتی رو برمی‌گردونه."""
        lam_self = self._lambda_vs(opponent)             # میانگین گل مورد انتظار خودمون برای ۹۰ دقیقه
        lam_opp = opponent._lambda_vs(self)               # همینطور برای حریف
        goals_self = int(np.random.poisson(lam_self))     # با پواسون تعداد گل واقعی رو تولید می‌کنیم
        goals_opp = int(np.random.poisson(lam_opp))         # همین کار برای گل‌های حریف

        pens = None   # فعلا نتیجه پنالتی نداریم، فقط اگه لازم شد پر میشه

        if is_knockout and goals_self == goals_opp:   # فقط توی مرحله حذفی، اگه ۹۰ دقیقه مساوی شد وقت اضافه داریم
            extra_self = int(np.random.poisson(lam_self * 0.33))   # توی وقت اضافه لامبدا خیلی کوچیک‌تر میشه
            extra_opp = int(np.random.poisson(lam_opp * 0.33))       # چون فقط ۳۰ دقیقه‌ست نه ۹۰ دقیقه
            goals_self += extra_self         # گل‌های وقت اضافه به نتیجه اصلی اضافه میشه
            goals_opp += extra_opp             # همینطور برای حریف

            if goals_self == goals_opp:            # اگه بازم بعد از وقت اضافه مساوی بود میره پنالتی
                p_self, p_opp, winner = self.penalty_shootout(opponent)
                pens = (p_self, p_opp)   # این رو نگه می‌داریم که بعدا توی نمایش نتیجه بشه نوشت "پنس"
            else:
                winner = self if goals_self > goals_opp else opponent   # وگرنه برنده با گل بیشتر مشخصه
        elif is_knockout:
            winner = self if goals_self > goals_opp else opponent   # حذفی بود ولی از همون ۹۰ دقیقه جواب گرفتیم
        else:
            # مرحله گروهیه، اینجا تساوی یه نتیجه‌ی کاملا قابل قبوله و نیازی به تعیین برنده نیست
            if goals_self > goals_opp:
                winner = self          # خودمون بردیم
            elif goals_opp > goals_self:
                winner = opponent      # حریف برد
            else:
                winner = None          # مساوی شد، همین کافیه

        return goals_self, goals_opp, winner, pens   # همه چیزی که Match کلاس بعدا بهش نیاز داره