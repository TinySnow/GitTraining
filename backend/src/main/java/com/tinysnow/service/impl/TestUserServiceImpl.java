package com.tinysnow.service.impl;

import io.mybatis.service.AbstractService;

import com.tinysnow.service.TestUserService;
import com.tinysnow.mapper.TestUserMapper;
import com.tinysnow.model.TestUser;
import org.springframework.stereotype.Service;

/**
 * test_user - 
 *
 * @author Snow
 */
@Service
public class  TestUserServiceImpl extends AbstractService<TestUser, Long, TestUserMapper> implements TestUserService {

}
