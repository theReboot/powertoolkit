import xlsxwriter


def get_format(wb, **kwargs):
    fmt = {
        'align': 'center',
        'bold': kwargs.get('b', False),
        'bg_color': kwargs.get('bg', 'white'),
        'size': kwargs.get('size', 14),
    }
    if 'valign' in kwargs:
        fmt.update({'valign': kwargs['valign']})
    if 'border' in kwargs:
        fmt.update({'border': kwargs['border']})
    if 'rotation' in kwargs:
        fmt.update({'rotation': kwargs['rotation']})
    if 'wrap' in kwargs:
        fmt.update({'text_wrap': 'wrap'})
    if 'fg' in kwargs:
        fmt.update({'font_color': kwargs['fg']})
    if 'num' in kwargs:
        fmt.update({'num_format': '#,##0'})
    return wb.add_format(fmt)


def download_status_data(rows, year, file_obj):
    workbook = xlsxwriter.Workbook(file_obj, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    fmt_title = get_format(workbook, size=14, b=True, fg='red')

    title = 'METERING STATUS FOR {}'.format(year)
    worksheet.merge_range('B3:F3', title, fmt_title)

    fmt_header = get_format(workbook, size=12, border=2, b=True, valign='top')
    fmt_footer = get_format(workbook, size=12, border=2, b=True)
    fmt_num_header = get_format(
        workbook, size=12, border=2, b=True, num=True)
    fmt_center = workbook.add_format({'align': 'center'})

    worksheet.set_column('B:B', 8, fmt_center)
    worksheet.set_column('C:C', 20, fmt_center)
    worksheet.set_column('D:G', 45, fmt_center)

    # set row heights and borders
    start_row = 3
    end_row = start_row + len(rows) + 1
    fmt_border = workbook.add_format({'align': 'center', 'num_format': '#,##0'})
    for row in rows:
        worksheet.set_row(row[0]+start_row, 30, fmt_border)
    worksheet.set_row(3, 30)
    worksheet.set_row(end_row, 30)

    # header
    worksheet.write_string(3, 1, 'S/N', fmt_header)
    worksheet.write_string(3, 2, 'DISCO NAME', fmt_header)
    worksheet.write_string(3, 3, 'TOTAL CUSTOMER COUNT', fmt_header)
    worksheet.write_string(3, 4, 'METERED CUSTOMER COUNT', fmt_header)
    worksheet.write_string(3, 5, 'METERING GAP', fmt_header)
    worksheet.write_string(3, 6, 'PERCENTAGE OF METERED CUSTOMERS', fmt_header)

    # footer
    worksheet.write_blank(end_row, 1, '', fmt_header)
    worksheet.write_string(end_row, 2, 'TOTAL', fmt_footer)
    total_summary = sum(row[2] for row in rows)
    worksheet.write_number(end_row, 3, total_summary, fmt_num_header)
    metered_summary = sum(row[3] for row in rows)
    worksheet.write_number(end_row, 4, metered_summary, fmt_num_header)
    gap_summary = sum(row[3] for row in rows)
    worksheet.write_number(end_row, 5, gap_summary, fmt_num_header)

    options = {
        'data': rows,
        'autofilter': False,
        'header_row': False,
        'banded_rows': False,
        'style': 'Table Style Light 11',
    }
    #worksheet.add_table('B5:G15', options)
    fmt_bordered = workbook.add_format({'border': 1, 'align': 'center', 'num_format': '#,##0'})
    for row in rows:
        worksheet.write_number(row[0]+start_row, 1, row[0], fmt_bordered)
        worksheet.write_string(row[0]+start_row, 2, row[1], fmt_bordered)
        worksheet.write_number(row[0]+start_row, 3, row[2], fmt_bordered)
        worksheet.write_number(row[0]+start_row, 4, row[3], fmt_bordered)
        worksheet.write_number(row[0]+start_row, 5, row[4], fmt_bordered)
        worksheet.write_string(row[0]+start_row, 6, row[5], fmt_bordered)

    workbook.close()
