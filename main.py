# محمدرضا یاری 404131333
# پروژه شبیه ساز جام جهانی 32 تیم

from world_cup_simulator import WorldCupSimulator   # کل منطق برنامه توی این کلاسه، اینجا فقط ازش استفاده می‌کنیم

def print_menu():
    """منوی اصلی برنامه رو توی خروجی چاپ می‌کنه."""
    print("\n===== World Cup Simulator =====")
    print("1) Load teams from CSV file")
    print("2) Run group draw (automatic seeding)")
    print("3) Run group stage and display each group's table")
    print("4) Run the full tournament (groups + knockout) and show the champion")
    print("5) Run 1000 simulations and report championship percentages")
    print("6) Display the knockout bracket of the last simulation")
    print("7) Exit")


def main():
    """حلقه اصلی برنامه، منو رو نشون میده و بر اساس انتخاب کاربر تابع مناسب رو صدا می‌زنه."""
    sim = WorldCupSimulator()   # یه نمونه از شبیه‌ساز که تا آخر برنامه همینو استفاده می‌کنیم
    while True:
        print_menu()
        choice = input("Please select an option (1-7): ").strip()   # ورودی کاربر رو می‌گیریم

        if choice == "1":
            filename = input("Enter the CSV file path (default: worldcup_2026_teams.csv): ").strip()
            sim.load_teams_from_csv(filename or "worldcup_2026_teams.csv")   # اگه چیزی ننوشت مسیر پیش‌فرض میره

        elif choice == "2":
            sim.groups_draw_and_seed()

        elif choice == "3":
            sim.stage_group_run()

        elif choice == "4":
            sim.simulation_full_run()

        elif choice == "5":
            raw = input("Enter the number of simulations (default: 1000): ").strip()
            try:
                num = int(raw) if raw else 1000   # ورودی خالی یعنی همون هزار بار پیش‌فرض
            except ValueError:
                print("Error: please enter a valid integer number.")   # مثلا کاربر حرف نوشته بود نه عدد
                continue
            sim.champion_likely_most(num)

        elif choice == "6":
            sim.bracket_display()

        elif choice == "7":
            print("Goodbye!")
            break   # از حلقه اصلی خارج میشیم و برنامه تموم میشه

        else:
            print("Invalid option. Please enter a number between 1 and 7.")   # هر عدد دیگه‌ای که تو رنج نبود


if __name__ == "__main__":
    main()   # فقط وقتی این فایل مستقیم اجرا بشه، نه وقتی import بشه یه جای دیگه