#include <iostream>

#include <alcommon/alproxy.h>
#include <alvalue/alvalue.h>

using namespace std;

int main(int argc, char**argv)
{
  // first argument must be host, second must be module name (RandomWalk/LineWalk)
  assert(argc >= 3);

  const string host = argv[1];
  const int port = 9559;
  const string module = argv[2];
  const string methodName = "start";

  AL::ALProxy observer("Observer", host, port);
  observer.callVoid("setLogFileNamePrefix", module);
  observer.callVoid(methodName);

  AL::ALProxy walker(module, host, port);
  walker.callVoid(methodName);

  return 0;
}
