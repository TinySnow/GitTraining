package com.tinysnow.controller;

import io.mybatis.common.core.DataResponse;
import io.mybatis.common.core.RowsResponse;

import com.tinysnow.model.TestUser;
import com.tinysnow.service.TestUserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * test_user - 
 *
 * @author Snow
 */
@RestController
@RequestMapping("testUsers")
public class TestUserController {

  @Autowired
  private TestUserService testUserService;

  @PostMapping
  public DataResponse<TestUser> save(@RequestBody TestUser testUser) {
    return DataResponse.ok(testUserService.save( testUser));
  }

  @GetMapping
  public RowsResponse<TestUser> findList(TestUser testUser) {
    return RowsResponse.ok(testUserService.findList( testUser));
  }

  @GetMapping(value = "/{id}")
  public DataResponse<TestUser> findById(@PathVariable("id") Long id) {
    return DataResponse.ok(testUserService.findById(id));
  }

  @PutMapping(value = "/{id}")
  public DataResponse<TestUser> update(@PathVariable("id") Long id, @RequestBody TestUser testUser) {
    testUser.setId(Math.toIntExact(id));
    return DataResponse.ok(testUserService.update( testUser));
  }

  @DeleteMapping(value = "/{id}")
  public DataResponse<Boolean> deleteById(@PathVariable("id") Long id) {
    return DataResponse.ok(testUserService.deleteById(id) == 1);
  }

}
