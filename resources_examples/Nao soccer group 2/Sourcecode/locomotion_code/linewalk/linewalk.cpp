#include "linewalk.hpp"
#include <qi/log.hpp>
#include <math.h>

using namespace std;

LineWalk::LineWalk(boost::shared_ptr<AL::ALBroker> broker,
                       const string& name)
  : AL::ALModule(broker, name)
{
  setModuleDescription("walk forward forever");

  functionName("start", getName(), "Just do it.");
  BIND_METHOD(LineWalk::start);
}

LineWalk::~LineWalk()
{
}

void LineWalk::init()
{
}

void LineWalk::start() {
  if (!posture.goToPosture("Stand", 1))
    throw "disappoint";

  // TODO: less stiff? maybe random stiffness?
  motion.setStiffnesses("Body", 1.0f);
  sleep(1);

  while (true) {
    vector<float> pose_before = motion.getRobotPosition(false);
    float x = 2, y = 0, theta = 0;

    qiLogInfo("LineWalk", "walking from (%f %f %f) to (%f %f %f)", pose_before[0], pose_before[1], pose_before[2], x, y, theta);
    // express the goal in FRAME_WORLD and store it in memory so that Observer can access it
    float rotcos = cos(pose_before[2]), rotsin = sin(pose_before[2]);
    float worldx = x * rotcos - y * rotsin + pose_before[0];
    float worldy = x * rotsin + y * rotcos + pose_before[1];

    memory.insertData("Module/Observer/goal/x", worldx);
    memory.insertData("Module/Observer/goal/y", worldy);
    memory.insertData("Module/Observer/hasgoal", 1.0f);

    motion.moveInit();
    motion.moveTo(x, y, theta);
    motion.waitUntilMoveIsFinished();

    memory.insertData("Module/Observer/hasgoal", -1.0f);
    memory.insertData("Module/Observer/goal/x", NaN);
    memory.insertData("Module/Observer/goal/y", NaN);

    // turn around
    motion.moveTo(0, 0, pose_before[2] + PI);

    sleep(1);
  }
}
