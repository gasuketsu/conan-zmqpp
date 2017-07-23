#include <iostream>
#include <string>
#include <cassert>
#include "zmqpp/zmqpp.hpp"

int main()
{
  zmqpp::context ctx;
  zmqpp::socket req(ctx, zmqpp::socket_type::request);
  zmqpp::socket rep(ctx, zmqpp::socket_type::reply);

  rep.bind("inproc://test.sock");
  req.connect("inproc://test.sock");

  zmqpp::message reqMsg;
  reqMsg << "hello";
  req.send(reqMsg);

  zmqpp::message receivedMsg;
  rep.receive(receivedMsg);
  assert(receivedMsg.get(0) == reqMsg.get(0));

  zmqpp::message repMsg;
  repMsg << "world";
  rep.send(repMsg);

  req.receive(receivedMsg);
  assert(receivedMsg.get(0) == repMsg.get(0));

  return 0;
}
