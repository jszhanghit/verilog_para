package Verilog_para;

require Exporter;
@ISA=qw(Exporter) ;
@EXPORT=qw(del_comment);

sub del_comment{
    

    my $content=$_[0] ;

    # 1: The comment is /* */ form,and the /* is happen in the front.
    # 0: The is no /* in the front
    my $flag = $_[1] ;

    if($flag){

        if($content=~/.*\*\//){
            $flag = 0 ;

            #将第一次出现的*/以及之前的信息删除
            $content =~ s#.*?\*/##;
            
            &del_comment($content,0);
        }
        else{
            $flag = 1 ;

            $content = "" ;
            return ($content,$flag) ;
        }

    }
    else #$flag == 0
    {
        # 有注释符
        if($content=~/\/\/|\/\*/){
            if($& eq "\/\/"){
                $content=~s#//.*##;
                return ($content,$flag) ;
            }
            else
            {
                #匹配的第一个注释符是 /* ,在字符串中又匹配到 */，则将/* xxx */删除，继续处理剩余字符
                if($content=~/\*\//)
                {
                    $content=~s#/\*.*?\*/##;
                    &del_comment($content,0);
                }
                else #如果没有匹配到*/则将/*后面的所有字符删除
                {
                    $content=~s#\\*.*##;
                    return ($content,1) ;
                }
            }
        }
        else # 没有注释符
        {
            return ($content,$flag) ;
        }
    }
}
1;
