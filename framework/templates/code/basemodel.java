/*
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
 *
 * Copyright (c) 2013-2016 Goja By Sogyf.
 */

package {{pkg}};

import com.jfinal.plugin.activerecord.Model;
import com.jfinal.plugin.activerecord.IBean;

/**
 * Table {{tableName}} base entities.
 * 
 * @author {{sysUser}}
 * @version 1.0
 * @since JDK 1.6
 */
public abstract class Base{{model}}<M extends Base{{model}}<M>> extends Model<M> implements IBean  {
    private static final long serialVersionUID = 1L;

    /* ---  Table fields defined.  --- */
    {% for _c in columns %}
    private {%if _c.data_type in ['int','smallint','tinyint','mediumint'] %} int     {% elif _c.data_type in ['varchar','char','text','longtext'] %} String {% elif _c.data_type in ['bit'] %} boolean {% elif _c.data_type in ['double'] %} double  {% elif _c.data_type in ['date','datetime'] %} java.util.Date {% elif _c.data_type in ['bigint'] %} long    {% elif _c.data_type in ['decimal','numeric'] %} java.math.BigDecimal {% else %} String {% endif %} {{_c.fieldvar}};{% endfor %}
    
    /* --- Fields Get And Set Method. ---  */
    {% for _c in columns %}{%if _c.data_type in ['int','smallint','tinyint','mediumint'] %}
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public int get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(int {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['varchar','char','text','longtext'] %}
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public String get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(String {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['bit'] %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public boolean is{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(boolean {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['double'] %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public double get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(double {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['date','datetime'] %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public java.util.Date get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(java.util.Date {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['bigint'] %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */    
    public long get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(long {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% elif _c.data_type in ['decimal','numeric'] %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public java.math.BigDecimal get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(java.math.BigDecimal {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% else %} 
    /**
     * The value of field [{{_c.name}}] was obtained from the query result set.
     * @return The value of field {{_c.name}}.
     */
    public String get{{_c.fieldName}}(){
        return get("{{_c.name}}");
    }

    /**
     * Set the value of field {{_c.name}}.
     * @param {{_c.fieldvar}} The Value.
     */
    public void set{{_c.fieldName}}(String {{_c.fieldvar}}){
        set("{{_c.name}}",{{_c.fieldvar}});
    }{% endif %}{% endfor %} 
}
