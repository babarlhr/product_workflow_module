
{
    'name' : 'Product workflow approval',
    'description' : 'This module adds workflow to the product. Installing this module will make you able to add extra level of rights',
    'author' : 'Muhammad Younis',
    'website' : 'https://www.upwork.com/freelancers/~01ca5bccf33e79e2f7',
    'category' : 'Inventory',
    'data' : ['views/workflow_view.xml','views/security_group.xml'],
    'depends' : ['product','stock','purchase','sale'],
    'installable' : True,
    'price' : '20',
    'currency' : 'EUR',
}