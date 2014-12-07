/*
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
 *
 * Copyright (c) 2013-2014 jfinal app. jfapp Group.
 */

package app.models;

import goja.annotation.TableBind;
import goja.plugins.sqlinxml.SqlKit;
import com.jfinal.plugin.activerecord.Model;

import java.util.List;

/**
 * <p>
 * The table {{tableName}} mapping model.
 * </p>
 */
@TableBind(tableName = "{{tableName}}")
public class {{model}} extends Model<{{model}}> {

    /**
     * The public dao.
     */
    public static final {{model}} dao = new {{model}}();


}