document.addEventListener("DOMContentLoaded", function () {

    /* ======================
       XP BAR ANIMATION
    ====================== */
    const xpBar = document.getElementById("xp-bar");
    if (xpBar) {
        const xp = parseInt(xpBar.dataset.xp || 0);
        const xpPerLevel = parseInt(xpBar.dataset.xpPerLevel || 100);
        const progress = Math.min((xp % xpPerLevel) / xpPerLevel * 100, 100);
        xpBar.style.transition = "width 1s ease-in-out";

        setTimeout(() => {
            xpBar.style.width = progress + "%";
        }, 100);
    }

    /* ======================
       HABIT COMPLETION EFFECT
    ====================== */
    const habitSoundEl = document.getElementById("habit-complete-sound");
    if (habitSoundEl) habitSoundEl.volume = 0.6;

    window.triggerHabitCompletionEffects = function(formEl = null) {
        // Play habit completion sound
        if (habitSoundEl) {
            habitSoundEl.currentTime = 0;
            habitSoundEl.play().catch(() => {});
        }

        // Confetti animation
        if (typeof confetti === "function") {
            const confettiDuration = 1500;
            const confettiEnd = Date.now() + confettiDuration;

            const confettiInterval = setInterval(() => {
                confetti({ particleCount: 6, angle: 60, spread: 55, origin: { x: 0 } });
                confetti({ particleCount: 6, angle: 120, spread: 55, origin: { x: 1 } });

                if (Date.now() > confettiEnd) clearInterval(confettiInterval);
            }, 200);
        }

        // Flash streak badge if available
        if (formEl) {
            const streakBadge = formEl.closest(".card")?.querySelector(".badge.streak");
            if (streakBadge) {
                streakBadge.classList.add("achievement-pulse");
                setTimeout(() => streakBadge.classList.remove("achievement-pulse"), 1200);
            }
        }
    };

    /* ======================
       ACHIEVEMENT UNLOCK EFFECT
    ====================== */
    const achievementSoundEl = document.getElementById("achievement-sound");
    if (achievementSoundEl) achievementSoundEl.volume = 0.6;

    window.triggerAchievementUnlock = function(newAchievementsSelector = ".new-achievement") {
        const achievements = document.querySelectorAll(newAchievementsSelector);
        if (!achievements.length) return;

        achievements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add("achievement-pulse");

                // Play sound only once for the first new achievement
                if (index === 0 && achievementSoundEl) {
                    achievementSoundEl.currentTime = 0;
                    achievementSoundEl.play().catch(() => {});
                }

                // Optional: confetti for each achievement
                if (typeof confetti === "function") {
                    confetti({ particleCount: 8, spread: 70 });
                }

                setTimeout(() => el.classList.remove("achievement-pulse"), 1200);

            }, index * 150);
        });
    };

    /* ======================
       Attach habit completion forms dynamically
    ====================== */
    document.querySelectorAll(".habit-complete-form").forEach(form => {
        form.addEventListener("submit", (e) => {
            window.triggerHabitCompletionEffects(form);
        });
    });

});

