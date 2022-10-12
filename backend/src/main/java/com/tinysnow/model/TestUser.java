package com.tinysnow.model;

import io.mybatis.provider.Entity;

import java.util.Date;

/**
 * test_user 
 *
 * @author Snow
 */
@Entity.Table(value = "test_user", autoResultMap = true)
public class TestUser {
  @Entity.Column(value = "id", id = true, remark = "", updatable = false, insertable = false)
  private Integer id;

  @Entity.Column(value = "name", remark = "")
  private String name;

  @Entity.Column(value = "password", remark = "")
  private String password;

  @Entity.Column(value = "birthday", remark = "", jdbcType = org.apache.ibatis.type.JdbcType.DATE)
  private Date birthday;

  @Entity.Column(value = "email", remark = "")
  private String email;


  /**
   * 获取 
   *
   * @return id - 
   */
  public Integer getId() {
    return id;
  }

  /**
   * 设置
   *
   * @param id 
   */
  public void setId(Integer id) {
    this.id = id;
  }

  /**
   * 获取 
   *
   * @return name - 
   */
  public String getName() {
    return name;
  }

  /**
   * 设置
   *
   * @param name 
   */
  public void setName(String name) {
    this.name = name;
  }

  /**
   * 获取 
   *
   * @return password - 
   */
  public String getPassword() {
    return password;
  }

  /**
   * 设置
   *
   * @param password 
   */
  public void setPassword(String password) {
    this.password = password;
  }

  /**
   * 获取 
   *
   * @return birthday - 
   */
  public Date getBirthday() {
    return birthday;
  }

  /**
   * 设置
   *
   * @param birthday 
   */
  public void setBirthday(Date birthday) {
    this.birthday = birthday;
  }

  /**
   * 获取 
   *
   * @return email - 
   */
  public String getEmail() {
    return email;
  }

  /**
   * 设置
   *
   * @param email 
   */
  public void setEmail(String email) {
    this.email = email;
  }

}
