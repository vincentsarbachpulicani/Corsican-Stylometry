<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:alto="http://www.loc.gov/standards/alto/ns-v3#"
    exclude-result-prefixes="#all"
    version="2.0">
    
    <xsl:output method="xml" version="1.0" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="/">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!--  x1=HPOS
          y1=VPOS
          x2=HPOS WIDTH
          y2=VPOS + HEIGHT
          x1,$y1 x2,y1 x2,y2 x1,y2 -->
    
    <xsl:template match="alto:TextLine">
        <xsl:variable name="x1" select="@HPOS"/>
        <xsl:variable name="y1" select="@VPOS"/>
        <xsl:variable name="x2" select="@HPOS + @WIDTH" />
        <xsl:variable name="y2" select="@VPOS + @HEIGHT" />
        <xsl:element name="TextLine" namespace="http://www.loc.gov/standards/alto/ns-v4#">
            <xsl:attribute name="BASELINE">
                <xsl:value-of select="$x1"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="$y2"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="$x2"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="$y2"/>
            </xsl:attribute>
            <xsl:apply-templates select="@*[name()!='BASELINE']"/>
            <xsl:element name="Shape" namespace="http://www.loc.gov/standards/alto/ns-v4#">
                <xsl:element name="Polygon" namespace="http://www.loc.gov/standards/alto/ns-v4#">
                    <xsl:attribute name="POINTS">
                        <xsl:value-of select="concat($x1,' ',$y1,' ',$x2,' ',$y1,' ',$x2,' ',$y2,' ',$x1,' ',$y2,' ',$x1,' ',$y1)"/>
                    </xsl:attribute>
                </xsl:element>
            </xsl:element>
            <xsl:apply-templates select="node()"/>
        </xsl:element>
    </xsl:template>
    
</xsl:stylesheet>