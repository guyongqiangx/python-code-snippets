import win32com.client as win32
import xml.etree.ElementTree as ET

'''
rule = [
    {
        'Name': 'JIRA Security',
        'Folder': 'JIRA Security',
        'SenderEmailAddress': 'DoNotReplyJIRA@broadcom.com',
        'Subject': None #'SWSECSUPRT'
    },
    {
        'Name': 'Tizen',
        'Folder': 'Tizen',
        'SenderEmailAddress': '@lists.tizen.org',
        'Subject': None
    },
]

srule = \
    {
        'Name': 'mtd mail list',
        'Folder': 'mtd mail list',
        'SenderEmailAddress': '@lists.infradead.org',
        'Subject': None
    }
'''


class Filter:
    def __init__(self, name, folder, email=None, subject=None):
        self.name = name
        self.folder = folder
        self.email = email
        self.subject = subject

    def _check_email(self, email=None):
        '''
        email patern seperator '|'
        :param email:
        :return:
        '''
        isMatch = False
        if self.email is None:
            isMatch = True
        elif email is not None:
            pat = self.email.split('|')
            for i in pat:
                if email.find(i) != -1:
                    isMatch = True
                    break
        else:
            isMatch = False
        return isMatch

    def _check_subject(self, subject=None):
        isMatch = False
        if self.subject is None:
            isMatch = True
        elif subject is not None and subject.find(self.subject) != -1:
            isMatch = True
        else:
            isMatch = False
        return isMatch

    def match(self, olmail=None, *, email=None, subject=None):
        if olmail is not None:
            email = None
            subject = None
            if hasattr(olmail, 'SenderEmailAddress'):
                email = olmail.SenderEmailAddress
            if hasattr(olmail, 'Subject'):
                subject = olmail.Subject

        return self._check_email(email) and self._check_subject(subject)

    def __str__(self):
        return '   Name: %s\n  Foler: %s\n  Email: %s\nSubject: %s\n' % (self.name, self.folder, self.email, self.subject)


class Rule:
    def __init__(self):
        self.filters = []

    def load(self, file=None, *, filters=None):
        if file is not None:
            rules = ET.parse(file)
            for filter in rules.findall('Filter'):
                name = filter.find('Name').text
                folder = filter.find('Folder').text
                email = filter.find('SenderEmailAddress').text
                subject = filter.find('Subject').text

                # only load filter if email or subject are set
                if email is not None or subject is not None:
                    item = Filter(name, folder, email, subject)
                    self.filters.append(item)
        elif filters is not None:
            for filter in filters:
                name = filter['Name']
                folder = filter['Folder']
                email = filter['SenderEmailAddress']
                subject = filter['Subject']

                item = Filter(name, folder, email, subject)
                self.filters.append(item)
        else:
            print('no filters provided')
        # show filters
        [print(item) for item in self.filters]

    def show(self, olmail=None):
        if olmail is not None:
            if hasattr(olmail, 'SenderEmailAddress'):
                print(olmail.SenderEmailAddress, olmail.Subject)
            else:
                print(olmail.Subject)

    def _get_folder(self, folder=None, filter=None):
        try:
            folder.Folders.Add(filter.folder)
        except:
            pass
        item = folder.Folders.Item(filter.folder)
        return item

    def _move(self, olmail=None, folder=None, filter=None):
        status = olmail.UnRead
        dest = self._get_folder(folder, filter)
        movedItem = olmail.Move(dest)
        movedItem.UnRead = True
        movedItem.Save()

        '''
        # find mail in new folder and restore read/unread status
        for mail in folder.Folders.Item(filter.folder).Items:
            if mail.ReceivedTime == time:
                mail.UnRead = status
        '''

    def apply_rule(self, olmail=None, folder=None, filter=None):
        if filter is not None:
            if filter.match(olmail):
                self.show(olmail)
                self._move(olmail, folder, filter)
                return True
        else:
            for item in self.filters:
                if item.match(olmail):
                    self.show(olmail)
                    self._move(olmail, folder, item)
                    return True
        return False

def sortemails():
    olook = win32.gencache.EnsureDispatch("Outlook.Application")
    ns = olook.GetNamespace("MAPI")

    inbox = ns.GetDefaultFolder(win32.constants.olFolderInbox)

    '''
    # load and apply rules from list
    myrule = Rule()
    myrule.load(file=None, filters=rule)
    for item in inbox.Items:
        myrule.apply_rule(item, inbox)
    '''

    myrule = Rule()
    myrule.load('rules.xml')

    '''
    # TODO: find the right way to enum inbox items, now try to use 'while' trick to check all items
    check = True
    while check:
        check = False
        for mail in inbox.Items:
            # TODO: need to check item type here!!
            check |= myrule.apply_rule(mail, inbox)
    '''

    max = inbox.Items.Count
    print('Total emails: %d' % max)
    # start to process from the last one to the first one
    for i in range(max, 1, -1):
        mail = inbox.Items[i]
        myrule.apply_rule(mail, inbox)

    '''
    # load and apply single rule
    filter = Filter(srule['Name'], srule['Folder'], srule['SenderEmailAddress'], srule['Subject'])
    for item in inbox.Items:
        myrule.apply_rule(item, inbox, filter)
    '''

    print('Done!')

if __name__ == '__main__':
    sortemails()
