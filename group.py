# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم
# کلاس مراحل گروهی

import random         # برای قرعه‌کشی پایه‌ی رتبه‌بندی وقتی همه‌چی مساویه لازمه
import functools       # برای اینکه تابع مقایسه‌ی رتبه‌بندی رو تبدیل کنم به کلید مرتب‌سازی
from match import Match   # هر گروه از کلاس Match برای اجرای بازی‌های داخلیش استفاده می‌کنه


class Group:
    """یه گروه ۴ تیمی، مسئول اجرای بازی‌های دور رفت و رتبه‌بندی نهاییه."""

    def __init__(self, name, teams):
        self.name = name                # اسم گروه، مثلا A یا B
        self.teams = teams              # لیست ۴ تیم عضو این گروه
        for t in teams:
            t.group = name              # به هر تیم هم میگیم توی کدوم گروهه، برای مرجع بعدی
        self.h2h = {}                    # نتیجه بازی مستقیم هر دو تیم رو اینجا نگه می‌داریم، برای شکستن تساوی
        self.cached_ranking = None        # وقتی یه بار رتبه‌بندی حساب شد دیگه دوباره تصادفی حسابش نمی‌کنیم

    def matches_all_play(self):
        """هر تیم دقیقا یک بار با ۳ تیم دیگه‌ی گروه بازی می‌کنه، یعنی جمعا ۶ بازی."""
        matches = []   # لیست بازی‌های این گروه رو برمی‌گردونیم که اگه لازم شد بشه استفاده کرد
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):   # با این حلقه تو در تو هر جفت تیم فقط یک بار انتخاب میشه
                m = Match(self.teams[i], self.teams[j])   # این بازی حذفی نیست، پس is_knockout پیش‌فرض False می‌مونه
                m.play()                                    # واقعا اجراش می‌کنیم
                matches.append(m)
                key = frozenset([self.teams[i].name, self.teams[j].name])   # کلید بدون توجه به ترتیب اسم‌ها
                self.h2h[key] = m.winner.name if m.winner else None   # نتیجه مستقیم رو ذخیره می‌کنیم برای بعد
        return matches

    def _h2h_score(self, a, b):
        # این تابع فقط میگه توی بازی مستقیم بین این دو تیم کی برنده بوده، برای شکستن تساوی نهایی به کار میاد
        res = self.h2h.get(frozenset([a.name, b.name]))
        if res == a.name:
            return 1    # یعنی a توی بازی مستقیم برده بوده، پس باید جلوتر بمونه
        if res == b.name:
            return -1   # برعکسش، b برنده بوده
        return 0        # یا مساوی بودن یا اصلا این دو تا با هم بازی نداشتن

    def ranking_get(self):
        """
        رتبه‌بندی نهایی چهار تیم گروه رو برمی‌گردونه. این نتیجه فقط یک بار محاسبه میشه و
        بعدش کش میشه، که مرحله حذفی دقیقا از همون تیم‌هایی استفاده کنه که مرحله گروهی مشخص کرده،
        نه یه محاسبه‌ی تصادفی جدید هر بار که این تابع صدا زده میشه.
        """
        if self.cached_ranking is not None:
            return self.cached_ranking   # اگه قبلا حساب شده همون رو برگردون، دوباره قرعه‌کشی نکن

        shuffled = self.teams[:]   # یه کپی از لیست تیم‌ها می‌گیریم که لیست اصلی دستکاری نشه
        random.shuffle(shuffled)   # این ترتیب تصادفی فقط برای وقتیه که همه معیارها کاملا مساوی باشن

        def cmp(a, b):
            if a.points != b.points:
                return b.points - a.points                     # اول از همه امتیاز بیشتر برنده‌ست
            if a.goal_difference() != b.goal_difference():
                return b.goal_difference() - a.goal_difference()   # بعد تفاضل گل بیشتر
            if a.for_goals != b.for_goals:
                return b.for_goals - a.for_goals                   # بعد گل زده بیشتر
            h2h = self._h2h_score(a, b)                              # اگه همه چی برابر بود بازی مستقیمشون رو نگاه کن
            if h2h != 0:
                return -h2h   # این یه قابلیت اضافه‌ست، شکستن تساوی با نتیجه رودررو قبل از قرعه‌کشی تصادفی
            return 0   # واقعا هیچ فرقی نداشتن، همون ترتیب تصادفی اولیه حفظ میشه

        self.cached_ranking = sorted(shuffled, key=functools.cmp_to_key(cmp))   # مرتب‌سازی نهایی و ذخیره در کش
        return self.cached_ranking

    def advance_teams(self):
        """دو تیم بالای جدول که به مرحله حذفی صعود می‌کنن رو برمی‌گردونه."""
        ranking = self.ranking_get()   # از همون رتبه‌بندی کش‌شده استفاده می‌کنیم
        return ranking[0], ranking[1]   # اول و دوم گروه

    def display_table(self):
        """جدول رده‌بندی گروه رو با فرمت خوانا چاپ می‌کنه."""
        print(f"===== Group {self.name} =====")   # عنوان گروه
        for i, t in enumerate(self.ranking_get(), start=1):   # از همون رتبه‌بندی که کش شده استفاده می‌کنیم
            print(f"{i}. {t.name}: {t.points} pts, GD {t.goal_difference():+d}, GF {t.for_goals}")