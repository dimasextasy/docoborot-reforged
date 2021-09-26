from stock.models import Product, DealProduct


def collect_data_for_report(deals_list, partner, date_data):
    name = partner.name
    surname = partner.surname
    patronymic = partner.patronymic
    company_name = partner.company_name

    deals_info = []
    for deal in deals_list:
        deal_products = DealProduct.objects.filter(deal_id=deal)
        for deal_product in deal_products:
            product = Product.objects.get(id=deal_product.product_id.id)
            product_dic = {
                'Дата': deal.date,
                'Продукт': product.name,
                'Количество': deal_product.count,
                'Цена продажи': product.selling_price,
                'Сумма': product.selling_price * deal_product.count
                }
            deals_info.append(product_dic)

    value = 0.00
    for element in deals_info:
        value += float(element['Сумма'])

    deals_info_group = {}
    for element in deals_info:
        if element['Дата'] not in deals_info_group.keys():
            deals_info_group.update({element['Дата']: []})
            deals_info_group[element['Дата']].append(
                {
                    "Продукт": element['Продукт'],
                "Количество": element['Количество'],
                "Цена продажи": element['Цена продажи'],
                "Сумма": element['Сумма']
                })

    report_info = {
    'Имя': name, 'Фамилия': surname, 'Отчество': patronymic,
    'Информация о закупках': deals_info_group,
    "Дата начала отсчета": date_data['start_date'], "Дата конца отсчета": date_data['finish_date'],
    "Компания": company_name, "Общая сумма закупок": value
    }
    return report_info
