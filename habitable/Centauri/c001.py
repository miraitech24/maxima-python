import numpy as np
import matplotlib.pyplot as plt

# C001: プロキシマ・ケンタウリ恒星フレア周期と遮蔽確率
# 物理コア: フレア頻度モデル（M5.5V型星）/ マイクロスロート開口部ダメージ率

# 定数
DAYS_PER_YEAR = 365.25
SECONDS_PER_DAY = 86400

# プロキシマ・ケンタウリのフレア統計（観測データに基づく）
# 平均フレア発生率: 約0.5回/日（小規模フレア）、大規模フレア: 約0.02回/日
small_flare_rate_per_day = 0.5  # 小規模フレア（エネルギー10^29 erg程度）
large_flare_rate_per_day = 0.02  # 大規模フレア（エネルギー10^31 erg以上）

# フレア継続時間（平均）
small_flare_duration_hours = 1.0  # 1時間程度
large_flare_duration_hours = 6.0  # 6時間程度

# マイクロスロート開口部の仕様
# 開口部直径: 10m（想定）
aperture_diameter_m = 10.0
aperture_area_m2 = np.pi * (aperture_diameter_m / 2) ** 2

# フレアによるダメージ閾値（エネルギー密度）
# 小規模フレア: 10^4 J/m^2 以上で軽度ダメージ
# 大規模フレア: 10^6 J/m^2 以上で重度ダメージ
damage_threshold_small_Jm2 = 1e4
damage_threshold_large_Jm2 = 1e6

# プロキシマbの軌道半径（0.0485 AU）
orbit_radius_AU = 0.0485
orbit_radius_m = orbit_radius_AU * 1.496e11

# フレアエネルギーが球状に拡散すると仮定
def energy_density_at_orbit(flare_energy_erg, distance_m):
    """フレアエネルギーが球状に拡散した場合のエネルギー密度[J/m^2]"""
    energy_J = flare_energy_erg * 1e-7  # erg -> J
    sphere_area = 4 * np.pi * distance_m ** 2
    return energy_J / sphere_area

# 小規模フレアのエネルギー密度
small_flare_energy_erg = 1e29
small_energy_density = energy_density_at_orbit(small_flare_energy_erg, orbit_radius_m)
print(f"小規模フレアのプロキシマb軌道でのエネルギー密度: {small_energy_density:.2e} J/m^2")

# 大規模フレアのエネルギー密度
large_flare_energy_erg = 1e31
large_energy_density = energy_density_at_orbit(large_flare_energy_erg, orbit_radius_m)
print(f"大規模フレアのプロキシマb軌道でのエネルギー密度: {large_energy_density:.2e} J/m^2")

# ダメージ判定
small_damage = small_energy_density > damage_threshold_small_Jm2
large_damage = large_energy_density > damage_threshold_large_Jm2
print(f"小規模フレアによる軽度ダメージ閾値超過: {small_damage}")
print(f"大規模フレアによる重度ダメージ閾値超過: {large_damage}")

# フレア遮蔽確率の計算
# マイクロスロート開口部がフレアの進行方向に対してどれだけ遮蔽されるか
# プロキシマbの半径: 約0.12地球半径
proxima_b_radius_m = 0.12 * 6.371e6  # 約764,520 m

# 開口部がプロキシマbの影に入る確率（幾何学的）
# 恒星から見たプロキシマbの立体角
solid_angle_planet = np.pi * (proxima_b_radius_m / orbit_radius_m) ** 2
total_solid_angle = 4 * np.pi
occultation_probability = solid_angle_planet / total_solid_angle
print(f"プロキシマbによる恒星遮蔽確率（幾何学的）: {occultation_probability:.6f}")

# 時間平均的な遮蔽確率（軌道周期考慮）
# プロキシマbの公転周期: 11.186日
orbital_period_days = 11.186
# 1日あたりの遮蔽時間（恒星の見かけの大きさから計算）
star_radius_proxima_m = 0.14 * 6.957e8  # 約0.14太陽半径
star_angular_radius = np.arctan(star_radius_proxima_m / orbit_radius_m)
planet_angular_radius = np.arctan(proxima_b_radius_m / orbit_radius_m)
# トランジット時間（恒星の中心を横切る場合）
transit_time_hours = (2 * (star_radius_proxima_m + proxima_b_radius_m) / 
                     (2 * np.pi * orbit_radius_m / (orbital_period_days * SECONDS_PER_DAY))) / 3600
print(f"最大トランジット時間: {transit_time_hours:.2f} 時間")

# 1日あたりの平均遮蔽時間
# 軌道傾斜角をランダムと仮定した場合の平均
average_occultation_hours_per_day = (transit_time_hours / orbital_period_days) * 24
print(f"1日あたりの平均遮蔽時間: {average_occultation_hours_per_day:.4f} 時間")

# フレア発生時の遮蔽確率
# フレア発生中に開口部が遮蔽されている確率
# フレア継続時間と遮蔽時間の重なりを考慮
def flare_occultation_probability(flare_duration_hours, occultation_hours_per_day):
    """フレア発生中に遮蔽されている確率"""
    # 単純化: フレア発生時刻がランダムと仮定
    return min(occultation_hours_per_day / 24, 1.0)

small_flare_occultation_prob = flare_occultation_probability(
    small_flare_duration_hours, average_occultation_hours_per_day)
large_flare_occultation_prob = flare_occultation_probability(
    large_flare_duration_hours, average_occultation_hours_per_day)

print(f"小規模フレア発生時の遮蔽確率: {small_flare_occultation_prob:.4f}")
print(f"大規模フレア発生時の遮蔽確率: {large_flare_occultation_prob:.4f}")

# 年間のフレア被曝回数とダメージ確率
days_per_year = 365.25
small_flares_per_year = small_flare_rate_per_day * days_per_year
large_flares_per_year = large_flare_rate_per_day * days_per_year

# 遮蔽なしで被曝するフレア数
small_flares_exposed = small_flares_per_year * (1 - small_flare_occultation_prob)
large_flares_exposed = large_flares_per_year * (1 - large_flare_occultation_prob)

print(f"\n年間小規模フレア発生数: {small_flares_per_year:.0f}")
print(f"年間大規模フレア発生数: {large_flares_per_year:.0f}")
print(f"遮蔽なしで被曝する小規模フレア数: {small_flares_exposed:.0f}")
print(f"遮蔽なしで被曝する大規模フレア数: {large_flares_exposed:.0f}")

# ダメージ確率（開口部がダメージ閾値を超える確率）
# 小規模フレア: 軽度ダメージ
small_damage_prob = 1.0 if small_damage else 0.0
# 大規模フレア: 重度ダメージ
large_damage_prob = 1.0 if large_damage else 0.0

# 年間ダメージ確率
annual_small_damage_prob = 1 - (1 - small_damage_prob * (1 - small_flare_occultation_prob)) ** small_flares_per_year
annual_large_damage_prob = 1 - (1 - large_damage_prob * (1 - large_flare_occultation_prob)) ** large_flares_per_year

print(f"\n年間軽度ダメージ確率: {annual_small_damage_prob:.4f}")
print(f"年間重度ダメージ確率: {annual_large_damage_prob:.4f}")

# グラフ: フレアエネルギーとダメージ閾値の関係
flare_energies = np.logspace(28, 32, 100)  # 10^28 ~ 10^32 erg
energy_densities = [energy_density_at_orbit(e, orbit_radius_m) for e in flare_energies]

plt.figure(figsize=(10, 6))
plt.loglog(flare_energies, energy_densities, 'b-', label='プロキシマb軌道でのエネルギー密度')
plt.axhline(y=damage_threshold_small_Jm2, color='orange', linestyle='--', label='軽度ダメージ閾値 (1e4 J/m²)')
plt.axhline(y=damage_threshold_large_Jm2, color='red', linestyle='--', label='重度ダメージ閾値 (1e6 J/m²)')
plt.xlabel('フレアエネルギー (erg)')
plt.ylabel('エネルギー密度 (J/m²)')
plt.title('プロキシマ・ケンタウリフレアエネルギーとマイクロスロート開口部ダメージ閾値')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('c001_flare_damage_analysis.png', dpi=150)
plt.close()

print("\nグラフを 'c001_flare_damage_analysis.png' に保存しました。")

# 結論
print("\n=== 結論 ===")
print(f"プロキシマb軌道での小規模フレアエネルギー密度: {small_energy_density:.2e} J/m²")
print(f"プロキシマb軌道での大規模フレアエネルギー密度: {large_energy_density:.2e} J/m²")
print(f"軽度ダメージ閾値(1e4 J/m²)を超える: {small_energy_density > damage_threshold_small_Jm2}")
print(f"重度ダメージ閾値(1e6 J/m²)を超える: {large_energy_density > damage_threshold_large_Jm2}")
print(f"年間軽度ダメージ確率: {annual_small_damage_prob*100:.1f}%")
print(f"年間重度ダメージ確率: {annual_large_damage_prob*100:.1f}%")
print(f"プロキシマbによる遮蔽確率: {occultation_probability*100:.2f}%")