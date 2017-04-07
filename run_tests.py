import prohow_functions as pf
import tests

print "BEGIN PROHOW COMPTENTENCY QUESTIONS TEST"

succeeded = 0
failed = 0

for name, val in tests.__dict__.iteritems():

    if callable(val):
        if val():
            succeeded += 1
            print "OK   "+val.__name__
        else:
            failed += 1
            print "FAIL " + val.__name__

print "FINISHED PROHOW COMPTENTENCY QUESTIONS TEST"

print str(succeeded)+"/"+str(succeeded+failed)

if failed == 0:
    print "ALL TESTS PASSED"
