"""
short_treasure_hunt.py
A shorter text-based treasure hunt game (interactive CLI).

Places:
1) Old Dock  -> get KEY (chance) + clue
2) Ancient Ruins -> solve riddle to get COMPASS
3) Dig Site -> win if you have KEY + COMPASS

 ┌───────────────┐
 │   START GAME  │
 └───────┬───────┘
         ↓
 ┌────────────────────┐
 │ Enter Player Name  │
 └─────────┬──────────┘
           ↓
 ┌─────────────────────────┐
 │ Choose Location         │
 │ (Dock / Ruins / Dig)    │
 └───────┬─────────┬───────┘
         │         │
         │         │
         │         │
         ↓         ↓
 ┌────────────┐  ┌───────────────┐
 │ OLD DOCK   │  │ ANCIENT RUINS │
 └─────┬──────┘  └──────┬────────┘
       │                 │
       │                 │
 ┌─────▼──────┐     ┌────▼────────┐
 │ Get OLD    │     │ Answer       │
 │ KEY? (70%) │     │ Riddle       │
 └─────┬──────┘     └────┬─────────┘
       │                 │
       │                 │
 ┌─────▼──────┐     ┌────▼────────┐
 │ KEY in     │     │ Correct?     │
 │ Inventory? │     └────┬────────┘
 └─────┬──────┘          │
       │                 │
       │            ┌────▼────────┐
       │            │ Get COMPASS │
       │            └────┬────────┘
       │                 │
       └───────────┬─────┘
                   ↓
          ┌───────────────────┐
          │   DIG SITE         │
          └─────────┬─────────┘
                    ↓
          ┌──────────────────────┐
          │ Use COMPASS + KEY ?  │
          └─────────┬────────────┘
                    │
          ┌─────────▼──────────┐
          │ YES → FIND TREASURE │
          │ 🏆 YOU WIN 🏆       │
          └────────────────────┘

"""

import random
def ask_choice(prompt, options):
    """Ask until user types a valid option (case-insensitive)."""
    options = [o.lower() for o in options]
    while True:
        print(prompt)
        print("Options:", ", ".join(options))
        choice = input("> ").strip().lower()
        if choice in options:
            return choice
        print("❌ Invalid choice. Try again.\n")


def add_item(inventory, item):
    """Add item to inventory if not already there."""
    if item not in inventory:
        inventory.append(item)
        print(f"✅ You obtained: {item}")
    else:
        print(f"ℹ️ You already have: {item}")


def show_status(inventory, clue):
    """Display inventory and clue."""
    print("\n📦 Inventory:", ", ".join(inventory) if inventory else "Empty")
    print("🧩 Clue:", clue if clue else "None")


# -----------------------------
# Places
# -----------------------------

def old_dock(inventory):
    print("\n⚓ OLD DOCK")
    print("You find a rusty box and a torn note stuck in a rope knot.")

    choice = ask_choice("What do you check?", ["box", "note", "leave"])

    clue = None

    if choice == "box":
        print("\n📦 The box is locked.")
        try_open = ask_choice("Try to force it open?", ["yes", "no"])
        if try_open == "yes":
            # 70% chance to get the key
            if random.random() < 0.7:
                print("🔓 The lock snaps open!")
                add_item(inventory, "OLD KEY")
            else:
                print("😬 It won’t open. Maybe try again later.")
        else:
            print("You leave the box alone.")

    elif choice == "note":
        print("\n📝 The note says: “STONE GUARDS THE GOLD.”")
        clue = "STONE GUARDS THE GOLD"

    else:
        print("\nYou step away from the dock.")

    return clue


def ancient_ruins(inventory, clue):
    print("\n🏛️ ANCIENT RUINS")
    print("A stone gate blocks the way. An inscription reads:")
    print("“Answer me to earn direction: What has hands but cannot clap?”")

    choice = ask_choice("What do you do?", ["answer", "leave"])

    if choice == "leave":
        print("You back away from the gate.")
        return

    answer = input("Your answer: ").strip().lower()

    if answer in ("clock", "a clock"):
        print("\n✅ The stone gate slides open!")
        print("Inside, you find a small compass with a carved arrow.")
        add_item(inventory, "COMPASS")
    else:
        print("\n❌ The gate does not move.")
        if clue:
            print(f"Hint from your clue: {clue} (think about 'stone' places!)")


def dig_site(inventory):
    print("\n🏝️ DIG SITE")
    print("You reach a hill marked by an X of stones.")

    choice = ask_choice("What do you do?", ["use compass", "dig randomly", "leave"])

    if choice == "leave":
        print("You decide not to dig right now.")
        return "continue"

    if choice == "use compass":
        if "COMPASS" in inventory and "OLD KEY" in inventory:
            print("\n🧭 The compass points to one exact spot.")
            print("⛏️ You dig... and hit a wooden chest!")
            print("🗝️ The OLD KEY fits perfectly.")
            print("🏆 YOU FOUND THE TREASURE! 🏆")
            return "win"
        missing = []
        if "COMPASS" not in inventory:
            missing.append("COMPASS")
        if "OLD KEY" not in inventory:
            missing.append("OLD KEY")
        print("\n❌ You can’t guarantee the right spot yet.")
        print("Missing:", ", ".join(missing))
        return "continue"

    # dig randomly
    print("\n⛏️ You dig at random spots...")
    if random.random() < 0.15:
        print("😱 Lucky hit! You found the chest by chance!")
        print("🏆 YOU WIN! 🏆")
        return "win"

    print("😩 Nothing here. Maybe you need better direction.")
    return "continue"


# -----------------------------
# Main loop
# -----------------------------

def play_game():
    print("\n==============================")
    print("🗺️ SHORT TREASURE HUNT")
    print("==============================")

    player = input("Explorer name: > ").strip() or "Explorer"
    inventory = []
    clue = None

    while True:
        show_status(inventory, clue)
        place = ask_choice(
            f"\nWhere do you go next, {player}?",
            ["old dock", "ruins", "dig site", "quit"]
        )

        if place == "old dock":
            new_clue = old_dock(inventory)
            if new_clue:
                clue = new_clue

        elif place == "ruins":
            ancient_ruins(inventory, clue)

        elif place == "dig site":
            result = dig_site(inventory)
            if result == "win":
                return "win"

        else:  # quit
            return "quit"


def main():
    while True:
        outcome = play_game()

        if outcome == "win":
            print("\n🎉 Congratulations! You completed the treasure hunt!\n")
        else:
            print("\n👋 You ended the hunt.\n")

        replay = ask_choice("Play again?", ["yes", "no"])
        if replay == "no":
            print("Thanks for playing! 🧭")
            break


if __name__ == "__main__":
    main()

