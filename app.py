import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

options_list = pd.read_csv('var.csv', sep=';')

selected_option = st.selectbox(
'Выбрать вариант для расчета',
(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30))

# Переменные из таблицы по вариантам
M = options_list.M.values[selected_option - 1] * 1000
V = options_list.V.values[selected_option - 1]
Z_r = options_list.Z_r.values[selected_option - 1]
C = options_list.C.values[selected_option - 1] * 1000
K = options_list.K.values[selected_option - 1] * 1000
a = options_list.a.values[selected_option - 1]
a_f = options_list.a_f.values[selected_option - 1]
K_ec = options_list.K_ec.values[selected_option - 1]
D = options_list.D.values[selected_option - 1]
K_ed = options_list.K_ed.values[selected_option - 1]

# Постоянные из текста
delta_T = 0.8
reserved_M = 0.1

alpha_min = 1.14
alpha_max = 1.2

E_n = 0.20
expected_demand = 1.25 * M

K_m = 0.85
lambda_tax = 0.215
beta_tax = 0.28

E_r = 0.17

# Формулы расчета показателей
# 1. Годовая производственная программа
q = round(K_m * M)
# 2. Ожидаемая цена одного кирпича
z = round((alpha_min + alpha_max) / 2 * Z_r, 4)
# 3. Годовая выручка от продажи одного кирпича
B = round(q * z)
# 4. Годовые переменные затраты предприятия
V_per = round(V * q)
# 5. Условно-постоянные затраты на единицу продукции
c = round(C / q, 5)
# 6. Себестоимость производства единицы продукции
s = round(V + c, 5)
# 7. Себестоимость годовой товарной продукции
S = round(s * q)
# 8. Годовая балансовая прибыль
P_b = round(q * (z - s))
# 9. Рентабельность изготовления кирпича
R_i = round((z - s) / s, 4)
# 10. Годовая производственная норма самоокупаемости деятельности предприятия
q_s = round(C / (z - V))
# 11. Характеристика и степень надежности будущего бизнеса. Отношения производственной мощности к программе самоокупаемости
relation_M_q_s = round(M / q_s, 2)
# 12. Величина годового совокупного налога предприятия
N = round(C * lambda_tax + P_b * beta_tax)
# 13. Годовая производственная программа самоокупаемости с учетом налогообложения
q_C = round((C * (1 + lambda_tax - beta_tax)) / ((z - V) * (1 - beta_tax)))
# 14. Доля, выручки, остающуюся в распоряжении у предприятия после выплаты налогов
O_p = round(1 - (q * (beta_tax * (z - V) + V) + C * (1 + lambda_tax - beta_tax)) / (q * z), 3)
# 15. Совокупный налог в процентах от балансовой прибыли
n = round(N / P_b, 3)
# 16. Коэффициент эффективности и срок окупаемости
E = round((P_b * (1 - n)) / (K + delta_T * P_b * (1 - n)), 2)
T = round(K / (P_b * (1 - n)) + delta_T, 2)
# Формулы Б части
# 1. Ожидаемая цена кирпича (индекс)
d = round(((1 + K_ec + K_ed * (D - 1) - a - a_f ) / K_ec) * (q / M), 6)
# 2. Ожидаемая цена в рублях
Z = round(z * d, 4)
# 3. Выручка предприятия
B_2 = round(q * Z)
# 6. Годовая балансовая прибыль
P_b_2 = round(q * (Z - s))
# 7. Рентабельность кирпича
R_i_2 = round((Z - s) / s, 4)
# 8. Годовой совокупный налог
N_2 = round(lambda_tax * C + beta_tax * P_b_2)
# 9. Доля выручки после налогов
O_p_2 = round(1 - (q * (beta_tax * (Z - V) + V) + C * (1 + lambda_tax - beta_tax)) / (q * Z), 4)
# 10. Совокупный налог в процентах от балансовой прибыли
n_2 = round(N / P_b, 4)
# 11. Коэффицент эффективности и срок окупаемости
E_2 = round((P_b_2 * (1 - n_2)) / (K + delta_T * P_b_2 * (1 - n_2)), 3)
T_2 = round(K / (P_b_2 * (1 - n_2)) + delta_T, 2)

summary_table = pd.DataFrame({
    'Наименование показателя': [
        '1 Годовая производственная программа, тыс. шт',
        '2 Цена за единицу продукции, руб./шт',
        '3 Годовая выручка предприятия, руб./год',
        '4 Годовые переменные затраты, руб./год',
        '5 Условно-постоянные затраты, руб./шт',
        '6 Себестоимость единицы продукции, руб./шт',
        '7 Себестоимость товарной продукции, руб./год',
        '8 Годовая балансовая прибыль, руб./год',
        '9 Рентабельность производства кирпича, %',
        '10 Производственная программа самоокупаемости, шт./год',
        '11 Поправочная норма эффективности на риск вложений',
        '12 Годовой совокупный налог, руб./год',
        '13 Производственная программа самоокупаемости с учетом налогообложения, шт./год',
        '14 Доля выручки, остающаяся в распоряжении предприятия, %',
        '15 Совокупный налог по отношению к балансовой прибыли, %',
        '16 Коэффициент эффективности капитальных затрат с учетом риска',
        '17 Срок окупаемости капитальных вложений, годы'
    ],
    'При затратном ценообразовании': [
        q/1000,
        z,
        B,
        V_per,
        c,
        s,
        S,
        P_b,
        R_i * 100,
        q_s,
        0.17,
        N,
        q_C,
        O_p * 100,
        n * 100,
        E,
        T
    ],
    'При рыночном ценообразовании': [
        q/1000,
        Z,
        B_2,
        V_per,
        c,
        s,
        S,
        P_b_2,
        R_i_2 * 100,
        q_s,
        0.17,
        N_2,
        q_C,
        O_p_2 * 100,
        n_2 * 100,
        E_2,
        T_2
    ]
})

K_m_percent = K_m * 100
q_line_1 = [K_m_percent, 0]
q_line_2 = [K_m_percent, q/1000]
revenue_1 = [0, 0]
revenue_2 = [85, B/1000]
fixed_costs1 = [0, C/1000]
fixed_costs2 = [85, C/1000]
variable_costs1 = [0, C/1000]
variable_costs2 = [85, (C + V_per)/1000]
permanent_tax1 = [0, (C + (C * lambda_tax))/1000]
permanent_tax2 = [85, (C + V_per + (C * lambda_tax))/1000]
variable_taxX = [(q_s/M) * 100, 100]
variable_taxY = [C/1000 + (V * (q_s/M * M))/1000 + (C * lambda_tax)/1000, (C + (V * M) + (C * lambda_tax + (M * (z - (V + C/M))) * beta_tax))/1000]

fig, ax = plt.subplots()

plt.xlabel('Уровень использования производственной мощности, %')
plt.ylabel('Затраты на производство, тыс. руб.')
ax.axline(q_line_1, q_line_2, color='k')
ax.axline(revenue_1, revenue_2, color='k')
ax.axline(fixed_costs1, fixed_costs2, color='k')
ax.axline(variable_costs1, variable_costs2, color='k')
ax.axline(permanent_tax1, permanent_tax2, color='k')
ax.plot(variable_taxX, variable_taxY, color='k')
ax.plot([(q_s/M) * 100, (q_s/M) * 100], [0, C/1000 + (V * (q_s/M * M))/1000 + (C * lambda_tax)/1000], color = 'k', linestyle='dashed')
ax.plot([(q_C/M) * 100, (q_C/M) * 100], [0, C/1000 + (V * (q_C/M * M))/1000 + (C * lambda_tax)/1000], color = 'k', linestyle = 'dashed')
plt.text(K_m_percent, 12200, f'q = {q} шт', fontsize = 12)
plt.text(40, B/1000/1.5, 'Выручка', fontsize = 12)
plt.text(80, C/1000/2, '1', fontsize = 12)
plt.text(80, (C + V_per)/1000/1.5, '2', fontsize = 12)
plt.text(80, (C + V_per + (C * lambda_tax))/1000/1.12, '4', fontsize = 12)
plt.text(80, (C + (V * M) + (C * lambda_tax + (M * (z - (V + C/M))) * beta_tax))/1000/1.27, '5', fontsize = 12)
plt.text(80, B/1000/1.2, '3', fontsize = 12)
ax.axis([0, 100, 0, 12000])

def main():
    cs_sidebar()
    cs_body()

    return None

def cs_sidebar():
    
    st.sidebar.header('Комплексная задача "Определение цены на изделие" по дисциплине "Экономика предприятия"')
    st.sidebar.markdown(r'''
        ## Условие
        Разработан технический проект строительства и эксплуатации кирпичного завода.

        Все расчеты необходимо произвести в двух вариантах \
        А. При затратном ценообразовании \
        Б. При рыночном ценообразовании

        ## Дано
        - $\Delta Т$ - период строительства и освоения производственных мощностей, лет
        - $M$ - производственная мощность завода, тыс.шт./год
        - $10\%$ признано использовать в качестве резерва
        - $C$ - постоянные расходы завода, тыс.руб./год
        - $V$ - переменные расходы, руб./шт
        - $Z_{р}$ - рыночная цена кирпича на момент проектирования завода, руб./шт
        - По прогнозируемым исследованиям, к началу эксплуатации завода цена кирпича изменится от $\alpha_{min} = 1.14$ до $\alpha_{max} = 1.2$ 
        - $K$ - капиталовложения в создание завода, тыс.руб
        - $E_{н}$ - норма эффективности капитальных вложений, установленная фирмой
        - Ожидаемый спрос на кирпич составляет $1.25M$
        - Величиной инфляции можно пренебречь

        - Планируемый выпуск кирпича составляет $85\%$ от производственной мощности предприятия $M$ => $K_{м} = 0,85M$ - коэффициент использования производственной мощности
        - Налоги определяются как $\lambda = 0.215$ величины постоянных затрат (условно-постоянные годовые налоги) и $\beta = 0.28$ балансовой прибыли предприятия (переменные налоги, зависящие от производственной деятельности предприятия)

        - $a$ - изменение товарной массы, поставляемой конкурентами на рынок, доли единицы
        - $a_{ф}$ - рыночная доля новой фирмы по отношению к объему товарной массы базового периода, доли единицы 
        - $K_{эц}$ - коэффициент ценовой эластичности спроса товара, доли единицы
        - $Д$ - коэффициент изменения дохода потребителей товара, доли единицы
        - $K_{эд}$ - коэффициент эластичности товара по доходу потребителей, доли единицы
    ''')

    return None

def cs_body():

    st.write('## Решение')
    st.write('### А. При затратном ценообразовании')

    # 1
    st.write(r'''
        1. Определим годовую производственную программу завода по формуле
        $$
        q = K_{м} \cdot M
        $$
    ''')
    st.write(f'$q = {K_m} \cdot {M} = {int(q/1000)}\ тыс.\ шт/год$')

    # 2
    st.write(r'''
        2. Определим ожидаемую цену одного кирпича по формуле
        $$
        z = \frac{\alpha_{min} + \alpha_{max}}{2} \cdot Z_{p}
        $$
    ''')
    st.write(f'$z = 0.5 \cdot ({alpha_min} + {alpha_max}) \cdot {Z_r} = {z}\ руб./год$')

    # 3
    st.write(r'''
        3. Определим годовую выручку от продажи кирпича по формуле
        $$
        B = q \cdot z
        $$
    ''')
    st.write(f'$B = {q} \cdot {z} = {B}\ руб./год $')

    # 4
    st.write(r'''
        4. Определим годовые переменные затраты предприятия по формуле
        $$
        V_{пер} = V \cdot q
        $$
    ''')
    st.write(r'$V_{пер}$', f'$= {V} \cdot {q} = {V_per}\ руб./год$')

    # 5
    st.write(r'''
        5. Определим условно-постоянные затраты на единицу продукции по формуле
        $$
        c = \frac{C}{q}
        $$
    ''')
    st.write(f'$ c= {C}\ /\ {q} = {c}\ руб./шт$')

    # 6
    st.write(r'''
        6. Определим себестоимость производства единицы продукции по формуле
        $$
        s = V + c
        $$
    ''')
    st.write(f'$s = {V} + {c} = {s}\ руб./шт$')

    # 7
    st.write(r'''
        7. Определим себестоимость годовой товарной продукции по формуле
        $$
        S = s \cdot q
        $$
    ''')
    st.write(f'$S = {s} \cdot {q} = {S}\ руб./год$')

    # 8 
    st.write(r'''
        8. Определим величину годовой балансовой прибыли предприятия по формуле
        $$
        П_{б} = q \cdot (z - s)
        $$
    ''')
    st.write(r'$П_{б}$', f'$= {q} \cdot ({z} - {s}) = {P_b}\ руб./год$')

    # 9
    st.write(r'''
        9. Определим рентабельность изготовления кирпича по формуле
        $$
        Р_{и} = \frac{z - s}{s}
        $$
    ''')
    st.write(r'$Р_{и}$',f'$= ({z} - {s}) /\ {s} = {R_i},\ или\ {R_i * 100}\%$')

    # 10
    st.write(r'''
        10. Определим годовую производственную программу самоокупаемости деятельности предприятия по формуле
        $$
        q_{s} = \frac{C}{z - V}
        $$
    ''')
    st.write(r'$q_{s}$', f'$= {C}\ /\ ({z} - {V}) = {q_s}\ шт./год$')

    # 11
    st.write(r'''
        11. Определим характеристику и степень надежности будущего бизнеса \
        Найдем отношение производственной мощности предприятия к производственной программе самоокупаемости
        $$
        \frac{M}{q_{s}}
        $$
    ''')
    st.write(f'${M}\ /\ {q_s} = {relation_M_q_s}$')

    # Промежуточный вывод
    st.write(r'''
        Полученная цифра свидетельствует, что бизнес опосредованно учитывает неопределенность будущей рыночной ситуации и будет достаточно надежным, так как его уровень риска ниже среднего, а поправочная норма эффективности
        капитальных затрат $E_{р}$, учитывающая риск вложений, составляет $0.17$
    ''')

    # 12
    st.write(r'''
        12. Определим величину годового совокупного налога предприятия (при отсутствии льгот по налогообложению) по формуле
        $$
        Н = Н_{пос} + Н_{пер} = C \cdot \lambda + П_{б} \cdot \beta
        $$
    ''')
    st.write(f'$Н = {C} \cdot {lambda_tax} + {P_b} \cdot {beta_tax} = {N}\ руб./год$')

    # 13
    st.write(r'''
        13. Определим годовую производственную программу самоокупаемости с учетом налогообложения по формуле
        $$
        q_{C} = \frac{C(1 + \lambda - \beta)}{(z - V)(1 - \beta)}
        $$
    ''')
    st.write(r'$q_{C}$', f'$= ({C}(1 + {lambda_tax} - {beta_tax}))\ /\ (({z} - {V})(1 -{beta_tax})) = {q_C}\ шт./год$')

    # Промежуточный вывод
    st.write(f'''
        Полученный результат свидетельствует о том, что с учетом налогообложения производственная программа самоокупаемости значительно возросла ($с\ {q_s}\ до\ {q_C}\ шт./год$), т.е. увеличилась в ${round(q_C / q_s, 1)}\ раз.$
        Это существенно сокращает величину чистой прибыли, повышает риск вложений в данный бизнес.
    ''')

    # 14
    st.write(r'''
        14. Определим долю выручки, остающуюся в распоряжении предприятия после выплаты налогов, по формуле
        $$
        О_{п} = 1 - \frac{q[\beta \cdot (z - V) + V] + C(1 + \lambda - \beta)}{q \cdot z}
        $$
    ''')
    st.write(r'$О_{п}$', f'$= 1 - ({q}[{beta_tax} \cdot ({z} - {V}) + {V}] + {C}(1 + {lambda_tax} - {beta_tax}))\ /\ ({q} \cdot {z}) = {O_p}, или\ {round(O_p * 100, 1)}\%$')

    # Промежуточный вывод
    st.write(f'''
        Это значит, что в распоряжении предприятия после выплаты налогов останется почти ${round(O_p * 100)}\%$ всей выручки, или ${O_p} \cdot {P_b} = {round(O_p * P_b)}\ руб./год.$
    ''')

    # 15
    st.write(r'''
        15. Определим совокупный налог в процентах от балансовой прибыли по формуле
        $$
        н = \frac{Н}{П_{б}}   
        $$
    ''')
    st.write(f'$н = {N}\ /\ {P_b} = {n},\ или\ {round(n * 100, 1)}\%$')

    # 16
    st.write(r'''
        16. Определим коэффициент эффективности и срок окупаемости капитальных вложений с учетом риска предпринимательства по следующим формулам
        $$
        E = \frac{П_{б} \cdot (1 - н)}{K + \Delta T \cdot П_{б} \cdot (1 - н)} > E_{н} + E_{р},
        $$
        $$
        T = \frac{K}{П_{б} \cdot (1 - н)} + \Delta T
        $$
        Подставим имеющиеся данные в формулу
    ''')
    st.write(f'$E = ({P_b} \cdot (1 - {n}))\ /\ ({K} + {delta_T} \cdot {P_b} \cdot (1 - {n})) = {E} > {E_n} + {E_r}$')
    st.write(r'''
        Следовательно, с учетом риска эффективность капитальных вложений полностью удовлетворяет требованиям теории и установленному предпринимателем ограничению нормы эффективности.
        Теперь можно определить срок окупаемости капитальных вложений
    ''')
    st.write(f'$T = {K}\ /\ ({P_b} \cdot (1 - {n})) + {delta_T} = {T}\ года$')

    st.write(r'''
        **Вывод**\
        Проект будущего бизнеса обеспечивает предпринимателю достаточно высокий доход и может быть рекомендован к реализации с учетом неопределенности будущей рыночной ситуации и риска вложений.\
        По расчетным данным построим график зависимости затрат и результатов производства от объема выпуска продукции, который в определенном масштабе представлен на рисунке.
    ''')

    st.pyplot(fig)
    st.write(r'''
        *Изменение результатов как функция объема производства при затратном ценообразовании:* \
        1 - условно-постоянные затраты; 2 - переменные затраты; 3 - чистая прибыль; 4 - постоянная часть налога; 5 - переменная часть налога; 3 + 4 + 5 - балансовая прибыль.
    ''')

    st.write('### Б. При рыночном ценообразовании')

    # 1
    st.write(r'''
        1. Прежде всего, надо по исходным данным и с учетом принятой производственнной производственной
            программы определить цену одного кирпича по следующей формуле
        $$
        d = \frac{1 + K_{эц} + K_{эд}(Д - 1) - a - a_{ф}}{K_{эц}}\cdot \frac{q}{M}
        $$
    ''')
    st.write(f'$d = ((1 + {K_ec} + {K_ed} \cdot ({D} - 1) - {a} - {a_f})\ /\ {K_ec}) \cdot ({q}\ /\ {M})  = {d}$')
    
    # 2
    st.write(r'''
        2. Так как полученная величина представляет не саму цену кирпича, а ее индекс, то для окончательного
            определения искомого значения цены необходимо провести следующую расчетную операцию
    ''')
    st.write(f'$Z = {z} \cdot {d} = {Z}\ руб./шт$')
    
    # 3
    st.write(r'''
        3. Определим выручку предприятия по формуле
        $$
        B = q * Z
        $$
    ''')
    st.write(f'$B = {q} \cdot {Z} = {B_2}\ руб./год$')
    
    # 4
    st.write(f'''
        4. Себестоимость одного кирпича остается без изменения, т.е. такой же, как и при затратном ценообразовании,
            и составляет
    ''')
    st.write(f'$s = {s}\ руб./шт$')
    
    # 5
    st.write(f'''
        5. Себестоимость годового товарного выпуска также остается без изменений
    ''')
    st.write(f'$S = {S}\ руб./год$')
    
    # 6
    st.write(r'''
        6. Определим годовую балансовую прибыль по формуле
        $$
        П_{б} = q \cdot (Z - s) 
        $$
    ''')
    st.write(r'$П_{б}$', f'$= {q} \cdot ({Z} - {s}) = {P_b_2}\ руб./год$')
    
    # 7
    st.write(r'''
        7. Определим рентабельность изготовления кирпича по формуле
        $$
        Р_{и} = \frac{(Z - s)}{s} 
        $$
    ''')
    st.write(r'$Р_{и}$', f'$= ({Z} - {s})\ /\ {s} = {R_i_2}$')
    
    # 8
    st.write(r'''
        8. Определим величину годового совокупного налога по формуле
        $$
        Н = \lambda \cdot C + \beta \cdot П_{б}
        $$
    ''')
    st.write(f'$Н = {lambda_tax} \cdot {C} + {beta_tax} \cdot {P_b_2} = {N_2}\ руб./год$')
    
    # 9
    st.write(r'''
        9. Определим долю выручки, остающуюся в распоряжении предприятия по формуле
        $$
        О_{п} = 1 - \frac{q \cdot [\beta \cdot (Z - V) + V] + C \cdot (1 + \lambda - \beta)}{q \cdot Z}
        $$
    ''')
    st.write(r'$О_{п}$', f'$= 1 - ({q} \cdot [{beta_tax} \cdot ({Z} - {V}) + {V}] + {C} \cdot (1 + {lambda_tax} - {beta_tax}))\ /\ ({q} \cdot {Z}) = {O_p_2}, или\ {round(O_p_2 * 100, 2)}\%$')
    st.write(f'''
        Таким образом, в распоряжении предприятия после расчета с бюджетом останется примерно
        ${round(O_p_2 * 100)}\%$ выручки, или ${O_p_2} \cdot {B_2} = {round(O_p_2 * B_2)}\ руб./год$
    ''')

    # 10
    st.write(r'''
        10. Определим совокупный налог в процентах от балансовой прибыли по формуле
        $$
        н = \frac{Н}{П_{б}}  
        $$
    ''')
    st.write(f'$н = {N_2}\ /\ {P_b_2} = {n_2},\ или\ {round(n_2 * 100, 2)}\%$')

    # 11
    st.write(r'''
        11. Определим коэффициент эффективности и срок окупаемости капитальных вложений по формулам
        $$
        E = \frac{П_{б} \cdot (1 - н)}{K + \Delta T \cdot П_{б} \cdot (1 - н)} > E_{н} + E_{р},
        $$
        $$
        T = \frac{K}{П_{б} \cdot (1 - н)} + \Delta T
        $$
        Подставим имеющиеся данные в формулу
    ''')
    st.write(f'$E = ({P_b_2} \cdot (1 - {n_2}))\ /\ ({K} + {delta_T} \cdot {P_b_2} \cdot (1 - {n_2})) = {E_2} > {E_n} + {E_r}$')
    st.write(f'$T = {K}\ /\ ({P_b_2} \cdot (1 - {n_2})) + {delta_T} = {T_2}\ года$')

    st.write(r'''
        **Вывод**
    ''')
    st.write(r'''
        Сравним расчетные результаты по затратному и рыночному ценообразованию между собой и представим
        всю информацию в таблице.
    ''')

    st.dataframe(summary_table, hide_index=True, use_container_width=False)

    st.write(r'*Вывод для 17 варианта:*')
    txt = st.text_area('', '''
        Исходя из полученных результатов, можно сделать вывод, что при рыночном ценообразовании показатели эффективности производства снижаются по сравнению с затратным ценообразованием. Это связано с тем, что при увеличении совокупной массы на рынке цена товара снижается, что приводит к ухудшению показателей, таких как выручка, балансовая прибыль, рентабельность производства и др.
        С другой стороны, в условиях рыночного ценообразования предприятие имеет меньше денег для дальнейшего развития после уплаты налогов. Однако, несмотря на это, можно считать, что предпринимательский проект является целесообразным и перспективным, а будущий бизнес — достаточно эффективным и надежным.
    ''', height=300)

    return None

# Run main()

if __name__ == '__main__':
    main()
