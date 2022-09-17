#!/usr/bin/env python
"""
使用指南：
默认每日热量缺口 400kcal
蔬菜不用记录，以及考虑到可能遗漏的热量（酱料等）格外增加缺口200 kcal
每个循环建议 3天低碳+一天高碳 高碳日做大肌群训练（腿臀），低碳日做小肌群胸肩背/有氧/休息
reference：https://youtu.be/b67tBfvb2Ks
"""

import argparse
import logging

def get_parser():
    """Returns the argparse parser to parse command-line options."""
    parser = argparse.ArgumentParser(
        description='daily diet plan calculator')
    parser.add_argument('--weight', action='store', type=int,
                        dest='weight',
                        help='weight in kg')
    parser.add_argument('--gender', action='store', type=str,
                        dest='gender',
                        help='male or female')
    parser.add_argument('--height', action='store', type=int,
                        dest='height',
                        help='height in cm')
    parser.add_argument('--age', action='store', type=int,
                        dest='age')
    parser.add_argument('--activity', action='store', type=int,
                        dest='activity_level', 
                        help='daily activity level 0-4')

    return parser.parse_args()

# activity level 0 - 4
# cal_delta: 热量缺口
# other_delta: 没算进去的蔬菜零食
def get_total_cal(height, weight, age, is_female, activity_level, cal_delta=400, other_delta=200):
    activity_multis = [1.2, 1.375, 1.55, 1.725, 1.9]
    if is_female:
        base = 655
        weight_multi = 9.6
        height_multi = 1.8
        age_multi = 4.7
    else:
        base = 66
        weight_multi = 13.7
        height_multi = 5
        age_multi = 6.8
    return (activity_multis[activity_level] * 
            (base + weight_multi * weight + height_multi * height - age_multi * age) - 
            (cal_delta + other_delta))

# 运动日 2倍体重
def get_protein(weight, activity_level=2):
    activity_multi = [1.5, 1.75, 2, 2.25, 2.5]
    return weight * activity_multi[activity_level]

def get_carb(is_high_carb, weight):
    return weight * 3 if is_high_carb else weight

def get_fat(total_cal, protein, carb):
    return (total_cal - (protein + carb) * 4) / 9
    
def get_daily_meal_plan(weight, height, age, is_female=True, activity_level=2, cal_delta=400, other_delta=200, high_carb_day=False):
    total_cal = get_total_cal(height, weight, age, is_female, activity_level)
    protein = get_protein(weight, activity_level)
    carb = get_carb(high_carb_day, weight)
    fat = get_fat(total_cal, protein, carb)
    print "  carb: %dg, protein: %dg, fat: %dg" % (carb, protein, fat)

def main():
    parsed_args = get_parser()
    weight = parsed_args.weight
    gender = parsed_args.gender or "female"
    age = parsed_args.age
    height = parsed_args.height
    activity_lv = parsed_args.activity_level
    is_female = True if gender == "female" else False
    
    print "Low Carb Day:"
    get_daily_meal_plan(weight, height=height, age=age, is_female=is_female, 
                        activity_level=activity_lv, high_carb_day=False)
    print "High Carb Day"
    get_daily_meal_plan(weight, height=height, age=age, is_female=is_female, 
                        activity_level=activity_lv, high_carb_day=True)
    
if __name__ == '__main__':
    main()
