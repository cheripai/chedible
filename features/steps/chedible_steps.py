from behave import *


@given(u'chedible is set up')
def flask_is_setup(context):
    assert context.client


@when(u'we visit the page')
def visit(context):
    context.page = context.client.get('/', follow_redirects=True)


@then(u'we should see the text "{text}"')
def text(context, text):
    assert text in str(context.page.data)
