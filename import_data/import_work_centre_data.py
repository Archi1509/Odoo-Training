import odoorpc
import openpyxl

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(odoo.db.list())

# Login
#odoo.login('db_name', 'user', 'passwd')
odoo.login('test', 'admin', 'admin')

# Current user
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name)# the name of its company

try:
    wb = openpyxl.load_workbook('/home/archi/Downloads/Work Centers.xlsx')
    ws = wb.active
    print(ws)

    for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                               max_col=None, values_only=True):
        # print(f"Record 0 {record[0]}, Record 1 {record[1]}, Record 2 {record[2]}, Record 3 {record[3]} ")
        tags = record[1].split(',')
        # print(tags)
        tag_ids=[]
        for tag in tags:
            search_tag = odoo.env['mrp.workcenter.tag'].search([('name', '=', tag)])
            if search_tag:
                tag_ids.append(search_tag[0])
            if not search_tag:
                created_tag_id = odoo.env['mrp.workcenter.tag'].create({
                    'name':tag
                })
                tag_ids.append(created_tag_id)

        if record[3]:
            alt_workcentres = record[3].split(',')
            created_alt_worksheet = []
            for alt_ws in alt_workcentres:
                search_alt_workcentre = odoo.env['mrp.workcenter'].search([('name', '=', record[3])])
                if search_alt_workcentre:
                    created_alt_worksheet.append(search_alt_workcentre[0])
                if not search_alt_workcentre:
                    create_alt_worksheet = odoo.env['mrp.workcenter'].create({
                        'name':alt_ws,
                    })
                    created_alt_worksheet.append(create_alt_worksheet)


            search_workcentre = odoo.env['mrp.workcenter'].search([('name', '=', record[0])])
            if not search_workcentre:
                rec = odoo.env['mrp.workcenter'].create({'name': record[0],
                                                         'tag_ids': [(6, 0, tag_ids)],
                                                         'code': record[2],
                                                         'alternative_workcenter_ids': [(6, 0, created_alt_worksheet)]
                                                         })
                # print(f"Record Created {rec}")
            else:
                work_rec = odoo.env['mrp.workcenter'].browse(search_workcentre[0])
                if work_rec:
                    work_rec.write({'tag_ids': [(6, 0, tag_ids)],
                                    'code': record[2],
                                    'alternative_workcenter_ids': [(6, 0, created_alt_worksheet)]
                                    })
                    # print(f"Record Updated {work_rec}")
        else:
            search_workcentre = odoo.env['mrp.workcenter'].search([('name', '=', record[0])])
            if not search_workcentre:
                rec = odoo.env['mrp.workcenter'].create({'name': record[0],
                                                         'tag_ids': [(6, 0, tag_ids)],
                                                         'code': record[2],
                                                         })
                # print(f"Record Created {rec}")
            else:
                work_rec = odoo.env['mrp.workcenter'].browse(search_workcentre[0])
                if work_rec:
                    work_rec.write({'tag_ids': [(6, 0, tag_ids)],
                                    'code': record[2],
                                    })
                    # print(f"Record Updated {work_rec}")




except Exception as e:
    print(f"Exception {e}")




