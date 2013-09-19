#pragma once

#include <alcommon/almodule.h>
#include <boost/shared_ptr.hpp>

#include <alproxies/almotionproxy.h>
#include <alproxies/almemoryproxy.h>
#include <alproxies/alrobotpostureproxy.h>

#include <limits>
#include <boost/math/constants/constants.hpp>

const float NaN = std::numeric_limits<float>::quiet_NaN();
const float PI = boost::math::constants::pi<float>();

namespace AL { class ALBroker; }

class LineWalk : public AL::ALModule
{
public:
  LineWalk(boost::shared_ptr<AL::ALBroker> broker, const std::string &name);
  ~LineWalk();
  void init();

  void start();

  AL::ALMotionProxy motion;
  AL::ALMemoryProxy memory;
  AL::ALRobotPostureProxy posture;
};
