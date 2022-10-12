package com.tinysnow.mapper;

import io.mybatis.mapper.Mapper;

import com.tinysnow.model.TestUser;

/**
 * test_user - 
 *
 * @author Snow
 */
@org.apache.ibatis.annotations.Mapper
public interface TestUserMapper extends Mapper<TestUser, Long> {

}