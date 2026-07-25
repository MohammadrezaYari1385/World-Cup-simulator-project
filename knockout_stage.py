# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم
# کلاس مراحل حذفی
class KnockoutStage:
    """یه مرحله از فاز حذفی، مثلا یک‌هشتم یا یک‌چهارم نهایی، با لیست بازی‌های همون مرحله."""

    def __init__(self, round_name, matches):
        self.round_name = round_name   # اسم مرحله برای نمایش، مثلا 'Round of 16'
        self.matches = matches          # لیست بازی‌های این مرحله

    def round_play(self):
        """همه بازی‌های این مرحله رو یکی‌یکی اجرا می‌کنه."""
        for m in self.matches:
            m.play()   # هر بازی جدا شبیه‌سازی و اجرا میشه

    def winners_get(self):
        """لیست برنده‌های این مرحله رو به همون ترتیب بازی‌ها برمی‌گردونه، برای ساخت مرحله بعدی لازمه."""
        return [m.winner for m in self.matches]

    def results_display(self):
        """خلاصه نتایج این مرحله رو چاپ می‌کنه."""
        print(f"===== {self.round_name} =====")
        for m in self.matches:
            print(m.result_string())   # از همون متد نمایش خود Match استفاده می‌کنیم